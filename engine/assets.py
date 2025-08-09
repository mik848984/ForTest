"""Helpers for loading game assets such as images."""

import os
import base64
import io

import pygame

from settings import ASSETS_DIR


# Embedded sprites encoded as Base64 strings.  This avoids shipping the
# binary PNG files with the project while still allowing easy access to the
# images at runtime.
EMBEDDED_SPRITES = {
    "snake.png": (
        "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGElEQVR4nGNk+M/wn4EIwESMolGF"
        "1FMIADydAhILOWPNAAAAAElFTkSuQmCC"
    ),
    "food.png": (
        "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGElEQVR4nGP8z8Dwn4EIwESMolGF"
        "1FMIAD2cAhK2AyPVAAAAAElFTkSuQmCC"
    ),
}


def get_asset_path(*paths):
    """Return absolute path to an asset inside the assets directory."""
    return os.path.join(ASSETS_DIR, *paths)


def load_sprite(filename: str) -> pygame.Surface:
    """Load a sprite image.

    The function first checks for an embedded Base64 encoded sprite.  If
    found, the data is decoded and loaded into a ``pygame.Surface`` with an
    alpha channel.  Otherwise the sprite is loaded from disk inside the
    ``assets`` directory.
    """

    if filename in EMBEDDED_SPRITES:
        data = base64.b64decode(EMBEDDED_SPRITES[filename])
        with io.BytesIO(data) as fh:
            return pygame.image.load(fh).convert_alpha()

    path = get_asset_path(filename)
    return pygame.image.load(path).convert_alpha()
