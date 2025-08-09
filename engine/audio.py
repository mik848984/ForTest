"""Audio management module for sound effects and music."""

import os
import math
import array
import pygame

from .assets import get_asset_path


class AudioManager:
    """Simple wrapper around ``pygame.mixer`` for handling audio."""

    def __init__(self, sound_dir: str | None = None) -> None:
        # Resolve directory with sound assets relative to the project
        default_dir = get_asset_path("sounds")
        self.sound_dir = sound_dir or default_dir
        self.sound_enabled = True
        self.effects: dict[str, pygame.mixer.Sound] = {}

        # Ensure mixer works even in headless environments
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        pygame.mixer.init()

    DEFAULT_BEEPS: dict[str, int] = {
        "food.wav": 880,
        "game_over.wav": 220,
        "wall.wav": 440,
        "victory.wav": 660,
    }

    def _generate_beep(self, frequency: int, duration: float = 0.2) -> pygame.mixer.Sound:
        sample_rate = 44100
        sample_count = int(sample_rate * duration)
        samples = array.array("h")
        for i in range(sample_count):
            value = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            samples.extend([value, value])  # stereo
        return pygame.mixer.Sound(buffer=samples)

    def load_effect(self, name: str, filename: str) -> None:
        """Load a sound effect or generate a simple beep if missing."""
        path = os.path.join(self.sound_dir, filename)
        if os.path.exists(path):
            self.effects[name] = pygame.mixer.Sound(path)
        else:
            freq = self.DEFAULT_BEEPS.get(filename, 440)
            self.effects[name] = self._generate_beep(freq)

    def play_effect(self, name: str) -> None:
        """Play a previously loaded sound effect if sound is enabled."""
        if self.sound_enabled and name in self.effects:
            self.effects[name].play()

    def play_music(self, filename: str, loops: int = -1) -> None:
        """Play background music file."""
        path = os.path.join(self.sound_dir, filename)
        if self.sound_enabled and os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops)

    def stop_music(self) -> None:
        pygame.mixer.music.stop()

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable all audio output."""
        self.sound_enabled = enabled
        if not enabled:
            self.stop_music()


# Global audio manager instance
audio = AudioManager()


__all__ = ["AudioManager", "audio"]

