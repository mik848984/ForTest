"""Utilities for loading models stored in the custom Permafrost format."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Mesh:
    """Simple representation of a mesh.

    The snake game does not render 3D models, but this data structure
    illustrates how Permafrost data could be consumed by another engine.
    """

    vertices: List[Tuple[float, float, float]]
    faces: List[Tuple[int, ...]]


def load_permafrost(path: str) -> Mesh:
    """Load a mesh from a Permafrost ASCII file."""
    with open(path, "r", encoding="utf-8") as fh:
        header = fh.readline().strip()
        if header != "permafrost_ascii 1.0":
            raise ValueError("Unsupported or corrupt file format")

        keyword, count = fh.readline().split()
        if keyword != "vertices":
            raise ValueError("Expected 'vertices' section")
        vertex_count = int(count)
        vertices = []
        for _ in range(vertex_count):
            x, y, z = map(float, fh.readline().split())
            vertices.append((x, y, z))

        keyword, count = fh.readline().split()
        if keyword != "faces":
            raise ValueError("Expected 'faces' section")
        face_count = int(count)
        faces = []
        for _ in range(face_count):
            indices = tuple(map(int, fh.readline().split()))
            faces.append(indices)

    return Mesh(vertices=vertices, faces=faces)
