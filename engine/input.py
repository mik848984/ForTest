import json
import os
import pygame

class InputManager:
    """Simple input manager that maps actions to keys or gamepad buttons."""

    def __init__(self, config_path: str = "controls.json") -> None:
        self.config_path = config_path
        self.bindings: dict[str, dict] = {}
        self.key_map: dict[int, str] = {}
        self.button_map: dict[int, str] = {}
        self.load()

    def load(self) -> None:
        """Load bindings from a JSON configuration file."""
        path = self.config_path
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.bindings = json.load(f)
        else:
            self.bindings = {}
        self._rebuild_maps()

    def save(self) -> None:
        """Persist current bindings to the configuration file."""
        path = self.config_path
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.bindings, f, ensure_ascii=False, indent=2)

    def _rebuild_maps(self) -> None:
        self.key_map.clear()
        self.button_map.clear()
        for action, mapping in self.bindings.items():
            key_name = mapping.get("keyboard")
            if key_name and hasattr(pygame, key_name):
                key = getattr(pygame, key_name)
                self.key_map[key] = action
            button = mapping.get("gamepad")
            if button is not None:
                self.button_map[int(button)] = action

    def get_action(self, event: pygame.event.Event) -> str | None:
        """Return the action mapped to a pygame event, if any."""
        if event.type == pygame.KEYDOWN:
            return self.key_map.get(event.key)
        if event.type == pygame.JOYBUTTONDOWN:
            return self.button_map.get(event.button)
        return None

    def set_binding(self, action: str, value, device: str = "keyboard") -> None:
        """Update binding for an action and device ('keyboard' or 'gamepad')."""
        self.bindings.setdefault(action, {})[device] = value
        self._rebuild_maps()
        self.save()
