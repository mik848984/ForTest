"""Rendering helpers used by the game engine.

This module now contains a very small camera implementation that can work
either in a classical top‑down mode or in a free mode similar to an FPS
camera.  The camera is intentionally lightweight – it merely stores its
position and exposes a method to transform world coordinates into screen
space.  The :class:`Renderer` uses this camera to offset draw calls.

The functionality is minimal but provides enough structure for games built on
top of this repository to experiment with different viewpoints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Camera:
    """Represents a very small 2D/3D camera.

    Only the features required for the exercises are implemented.  The camera
    supports two modes:

    ``"topdown"``
        A classical RTS style camera where only the ``x`` and ``y`` position is
        taken into account.

    ``"free"``
        A simplified FPS style camera that additionally tracks the ``z`` axis.
        The ``z`` value is currently unused by the renderer but is provided so
        that game code can build upon it if needed.
    """

    mode: str = "topdown"
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    def move(self, dx: float, dy: float, dz: float = 0.0) -> None:
        """Move the camera by the given deltas."""

        x, y, z = self.position
        if self.mode == "topdown":
            self.position = (x + dx, y + dy, z)
        else:
            self.position = (x + dx, y + dy, z + dz)

    def apply(self, x: float, y: float) -> Tuple[float, float]:
        """Translate world coordinates to screen coordinates."""

        cx, cy, _ = self.position
        return x - cx, y - cy


class Renderer:
    """Very small renderer that works together with :class:`Camera`."""

    def __init__(self, surface=None, camera: Camera | None = None) -> None:
        # ``surface`` is expected to be a pygame surface, but pygame is only
        # required by the caller.  Keeping the dependency optional makes the
        # renderer easier to test.
        self.surface = surface
        self.camera = camera or Camera()

    def begin(self) -> None:
        """Prepare rendering."""

        # For pygame this would typically fill the background.  Since this
        # project mainly uses unit tests without an actual display we simply
        # return ``None`` to keep the API consistent.
        return None

    def end(self) -> None:
        """Finalize rendering."""

        # When using pygame the caller would usually flip the display here.
        return None

    # The *args and **kwargs* interface is kept so existing code continues to
    # work.  The method now respects the camera's position and offsets the
    # coordinates before delegating to pygame (if a surface is present).
    def draw(self, surface, position: Tuple[float, float]) -> None:
        """Draw ``surface`` at ``position`` taking the camera into account."""

        if self.surface is None:
            return None
        x, y = self.camera.apply(*position)
        self.surface.blit(surface, (x, y))
        return None

