import os
import sys
import pytest

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game.snake import Snake
from game.level import Level
from game.score import ScoreManager


def test_snake_grows_when_food_eaten():
    snake = Snake()
    level = Level()
    score = ScoreManager(level)

    # Snake grows when score manager emits food eaten event
    score.on_food_eaten.append(lambda s: snake.grow())
    initial_len = len(snake.body)

    score.eat_food()
    snake.move()

    assert len(snake.body) == initial_len + 1


def test_collision_with_self_triggers_game_over_event():
    snake = Snake(initial_length=3, start_pos=(2, 2))
    # Manually create self-collision
    snake.body = [(1, 1), (1, 2), (1, 1)]

    score = ScoreManager(Level())
    triggered = []
    score.on_game_over.append(lambda: triggered.append(True))

    if snake.check_self_collision():
        score.game_over()

    assert triggered  # event fired


def test_wall_collision_detection():
    snake = Snake(initial_length=1, start_pos=(0, 0))
    snake.direction = (-1, 0)  # force movement towards the wall
    snake.move()

    assert snake.check_wall_collision(width=10, height=10)


def test_level_transitions_on_score():
    level = Level(threshold=2)
    score = ScoreManager(level)

    score.eat_food()
    assert level.level == 1

    score.eat_food()
    assert level.level == 2
