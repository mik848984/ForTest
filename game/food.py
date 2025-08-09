"""Food module providing the :class:`Food` class."""
from __future__ import annotations

import random
from typing import Iterable, Tuple

Position = Tuple[int, int]


class Food:
    """Represents food that the snake can eat."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.position: Position = (0, 0)
        self.spawn([])

    def spawn(self, occupied: Iterable[Position]) -> Position:
        """Place the food at a random location not in *occupied*."""
        while True:
            pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if pos not in occupied:
                self.position = pos
                return pos
