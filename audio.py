import os
import pygame


class AudioManager:
    """Simple wrapper around pygame.mixer for sound effects and music."""

    def __init__(self, sound_dir=None):
        # Path to directory with sound assets
        default_dir = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')
        self.sound_dir = sound_dir or default_dir
        self.sound_enabled = True
        self.effects = {}
        # Initialize mixer only once
        pygame.mixer.init()

    def load_effect(self, name, filename):
        """Load a sound effect from assets."""
        path = os.path.join(self.sound_dir, filename)
        if os.path.exists(path):
            self.effects[name] = pygame.mixer.Sound(path)

    def play_effect(self, name):
        """Play a loaded sound effect if sound is enabled."""
        if self.sound_enabled and name in self.effects:
            self.effects[name].play()

    def play_music(self, filename, loops=-1):
        """Play background music from file."""
        path = os.path.join(self.sound_dir, filename)
        if self.sound_enabled and os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_enabled(self, enabled: bool):
        """Globally enable or disable sound."""
        self.sound_enabled = enabled
        if not enabled:
            self.stop_music()


# Global audio manager instance
audio = AudioManager()
