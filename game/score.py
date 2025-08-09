"""Score and event management for the snake game."""
from __future__ import annotations

from typing import Callable, List, Optional

from .level import Level


class ScoreManager:
    """Manages score and emits game events."""

    def __init__(self, level: Optional[Level] = None) -> None:
        self.score = 0
        self.high_score = 0
        self.level = level or Level()
        self.on_food_eaten: List[Callable[[int], None]] = []
        self.on_game_over: List[Callable[[], None]] = []

    def eat_food(self) -> None:
        """Increase score and notify listeners."""
        self.score += 1
        self.level.update(self.score)
        for cb in list(self.on_food_eaten):
            cb(self.score)

    def game_over(self) -> None:
        """Reset state and notify listeners of game over."""
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.level.reset()
        for cb in list(self.on_game_over):
            cb()
