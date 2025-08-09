"""Snake module providing the :class:`Snake` class."""
from __future__ import annotations

from typing import List, Tuple

Position = Tuple[int, int]


class Snake:
    """Represents the snake on the game field.

    The snake consists of a list of grid positions.  Movement happens by
    inserting a new head in the current direction and removing the last
    element unless growth has been triggered with :meth:`grow`.
    """

    def __init__(self, initial_length: int = 3, start_pos: Position = (5, 5)) -> None:
        self.direction: Position = (1, 0)
        x, y = start_pos
        # Create body extending to the left from the starting point
        self.body: List[Position] = [(x - i, y) for i in range(initial_length)]
        self._growth: int = 0

    def head(self) -> Position:
        """Return the current head position."""
        return self.body[0]

    def set_direction(self, direction: Position) -> None:
        """Change movement direction if it is not opposite to current."""
        dx, dy = direction
        cx, cy = self.direction
        if (dx, dy) != (-cx, -cy):
            self.direction = (dx, dy)

    def move(self) -> Position:
        """Advance the snake one cell and return new head position."""
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if self._growth:
            self._growth -= 1
        else:
            self.body.pop()
        return new_head

    def grow(self, amount: int = 1) -> None:
        """Trigger the snake to grow by *amount* cells on next moves."""
        self._growth += amount

    # Collision helpers -------------------------------------------------
    def check_self_collision(self) -> bool:
        """Return ``True`` if the snake's head intersects its body."""
        return self.head() in self.body[1:]

    def check_wall_collision(self, width: int, height: int) -> bool:
        """Return ``True`` if the snake's head is outside the play field."""
        x, y = self.head()
        return x < 0 or y < 0 or x >= width or y >= height
