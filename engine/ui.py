"""Small UI helpers based on an immediate mode approach.

The real project would make use of the `nuklear` Python bindings to display UI
widgets.  Shipping the full dependency is unnecessary for the unit tests, so
this module implements just enough to render a score and high‑score counter on a
pygame surface.  The API intentionally mirrors a tiny subset of what a Nuklear
interface might look like so game code can be written in a similar style.
"""

from __future__ import annotations

from dataclasses import dataclass
import pygame


@dataclass
class ScoreUI:
    """Utility to render the current score and record."""

    surface: pygame.Surface
    font: pygame.font.Font | None = None

    def __post_init__(self) -> None:  # pragma: no cover - trivial
        if self.font is None:
            self.font = pygame.font.Font(None, 24)

    def draw(self, score: int, high_score: int) -> None:
        """Render ``score`` and ``high_score`` on the associated surface."""

        score_surf = self.font.render(f"Score: {score}", True, (255, 255, 255))
        high_surf = self.font.render(f"Record: {high_score}", True, (255, 255, 0))
        self.surface.blit(score_surf, (10, 10))
        self.surface.blit(high_surf, (10, 32))
