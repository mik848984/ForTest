"""Utility for exporting models to the custom Permafrost ASCII format.

This script is intended to be executed inside Blender:
    blender --background --python blender_scripts/export_permafrost.py -- \
        --input path/to/model.obj --output path/to/model.pfr --decimate 0.5

Steps performed:
1. Import OBJ or FBX model and its materials.
2. Optionally reduce polygon count using the Decimate modifier.
3. Generate a basic UV unwrap.
4. Export vertices and face indices to a simple ASCII file understood by the
   engine's ``load_permafrost`` helper.
"""

import argparse
import os
import sys

import bpy
import bmesh


def parse_args() -> argparse.Namespace:
    """Parse command line arguments passed after ``--``."""
    parser = argparse.ArgumentParser(description="Export model to Permafrost format")
    parser.add_argument("--input", required=True, help="Path to OBJ/FBX model")
    parser.add_argument("--output", required=True, help="Destination .pfr file")
    parser.add_argument("--decimate", type=float, default=1.0, help="Optional decimation ratio (0-1)")

    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1 :]
    else:
        argv = []
    return parser.parse_args(argv)


def import_model(path: str) -> bpy.types.Object:
    """Import the model and return the created object."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".obj":
        bpy.ops.import_scene.obj(filepath=path)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    return bpy.context.selected_objects[0]


def optimize_mesh(obj: bpy.types.Object, ratio: float) -> None:
    """Apply decimation and unwrap UVs."""
    bpy.context.view_layer.objects.active = obj
    if 0 < ratio < 1.0:
        mod = obj.modifiers.new(name="Decimate", type="DECIMATE")
        mod.ratio = ratio
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def export_permafrost(obj: bpy.types.Object, filepath: str) -> None:
    """Write vertex and face data to an ASCII Permafrost file."""
    mesh = obj.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write("permafrost_ascii 1.0\n")
        fh.write(f"vertices {len(bm.verts)}\n")
        for v in bm.verts:
            fh.write(f"{v.co.x} {v.co.y} {v.co.z}\n")

        bm.faces.ensure_lookup_table()
        fh.write(f"faces {len(bm.faces)}\n")
        for face in bm.faces:
            indices = " ".join(str(v.index) for v in face.verts)
            fh.write(f"{indices}\n")

    bm.free()


def main() -> None:
    args = parse_args()
    obj = import_model(args.input)
    optimize_mesh(obj, args.decimate)
    export_permafrost(obj, args.output)
    print("Permafrost export finished:", args.output)


if __name__ == "__main__":
    main()
