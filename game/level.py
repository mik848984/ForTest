"""Level management for the snake game."""
from __future__ import annotations

from typing import Callable, List


class Level:
    """Tracks the current level and handles level up events."""

    def __init__(self, threshold: int = 5) -> None:
        self.threshold = threshold
        self.level = 1
        self.on_level_up: List[Callable[[int], None]] = []

    def reset(self) -> None:
        self.level = 1

    def update(self, score: int) -> None:
        """Update level based on *score* and fire events if needed."""
        required = self.level * self.threshold
        if score >= required:
            self.level += 1
            for cb in list(self.on_level_up):
                cb(self.level)
