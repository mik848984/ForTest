import os
import sys
import pygame
import pytest

# Ensure project root on path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine.assets import load_sprite


@pytest.fixture(scope="module", autouse=True)
def _pygame_setup():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def test_load_snake_sprite_from_base64():
    sprite = load_sprite("snake.png")
    assert sprite.get_size() == (10, 10)
    assert sprite.get_at((0, 0)) == pygame.Color(0, 255, 0, 255)


def test_load_food_sprite_from_base64():
    sprite = load_sprite("food.png")
    assert sprite.get_size() == (10, 10)
    assert sprite.get_at((0, 0)) == pygame.Color(255, 0, 0, 255)
