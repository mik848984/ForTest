"""Input handling helpers.

The original project only exposed a very small stub.  This file now contains a
fully working input handler built on top of :mod:`pygame`.  It converts pygame
events into a simplified representation understood by the engine.  Moving the
keyboard handling into this module decouples game code from pygame’s global
event queue and makes it easier to swap out the backend if necessary.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

try:  # pragma: no cover - pygame is optional for some unit tests
    import pygame
except Exception:  # pragma: no cover
    pygame = None  # type: ignore


@dataclass
class Event:
    """Simplified input event structure."""

    type: str
    key: int | None = None
    user_type: int | None = None


class InputHandler:
    """Collects and normalises user input."""

    def get_events(self) -> List[Event]:
        """Return a list of :class:`Event` objects.

        Each pygame event is converted into a small ``Event`` dataclass.  Only
        the attributes commonly used by the examples are exposed.  Unsupported
        event types are ignored which keeps the interface pleasantly small.
        """

        if pygame is None:  # Pygame not available (e.g. during docs build)
            return []

        events: List[Event] = []
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                events.append(Event("quit"))
            elif ev.type == pygame.KEYDOWN:
                events.append(Event("key_down", key=ev.key))
            elif ev.type == pygame.KEYUP:
                events.append(Event("key_up", key=ev.key))
            elif ev.type >= pygame.USEREVENT:
                events.append(Event("user", user_type=ev.type))
        return events

