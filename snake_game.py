import pygame
import random
import sys
from pygame import Vector2

import audio
from engine.input import InputHandler
from engine.ui import ScoreUI

# Инициализация Pygame
pygame.init()

# Константы игры
CELL_SIZE = 40
CELL_NUMBER = 20
SCREEN_SIZE = CELL_SIZE * CELL_NUMBER

# Цвета
BACKGROUND_COLOR = (100, 150, 255)  # Синий цвет фона
SNAKE_COLOR = (83, 224, 73)
FOOD_COLOR = (255, 0, 0)
SCORE_COLOR = (56, 74, 12)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('🐍 Змейка - 2D Игра')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        
        # Загрузка изображений змейки
        self.head_up = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_up.fill(SNAKE_COLOR)
        self.head_down = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_down.fill(SNAKE_COLOR)
        self.head_right = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_right.fill(SNAKE_COLOR)
        self.head_left = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.head_left.fill(SNAKE_COLOR)
        
        self.tail = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.tail.fill(SNAKE_COLOR)
        
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, block_rect)
    
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)

class Food:
    def __init__(self):
        self.randomize()
        
    def draw_food(self):
        food_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, food_rect)
    
    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = 0
        self.game_active = False
        self.settings_active = False
        self.sound_enabled = True

        # load sound effects
        audio.audio.load_effect('food', 'food.wav')
        audio.audio.load_effect('game_over', 'game_over.wav')

        # Engine subsystems
        self.input = InputHandler()
        self.ui = ScoreUI(screen)
        
    def update(self):
        if self.game_active:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()
    
    def draw_grass(self):
        grass_color = (80, 120, 200)  # Более тёмный синий для узора
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    
    def check_collision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize()
            self.snake.add_block()
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.on_food_eaten()
        
        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.randomize()
    
    def check_fail(self):
        # Прохождение через стены
        if self.snake.body[0].x < 0:
            self.snake.body[0].x = CELL_NUMBER - 1
        elif self.snake.body[0].x >= CELL_NUMBER:
            self.snake.body[0].x = 0
        elif self.snake.body[0].y < 0:
            self.snake.body[0].y = CELL_NUMBER - 1
        elif self.snake.body[0].y >= CELL_NUMBER:
            self.snake.body[0].y = 0
        
        # Проверка столкновения с собой
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        self.game_active = False
        self.snake.reset()
        self.food.randomize()
        self.score = 0
        self.on_game_over()
    
    def draw_score(self):
        self.ui.draw(self.score, self.high_score)

    def start_game(self):
        self.game_active = True
        if self.sound_enabled:
            audio.audio.play_music('music.mp3')

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        audio.audio.set_enabled(self.sound_enabled)
        if self.sound_enabled and self.game_active:
            audio.audio.play_music('music.mp3')

    def draw_settings(self):
        font = pygame.font.Font(None, 74)
        title_surface = font.render('Настройки', True, SCORE_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 - 80))
        screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, 50)
        sound_text = f'Звук: {"Вкл" if self.sound_enabled else "Выкл"}'
        sound_surface = font.render(sound_text, True, SCORE_COLOR)
        sound_rect = sound_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2))
        screen.blit(sound_surface, sound_rect)

        instruction_surface = font.render('Нажмите S для переключения', True, SCORE_COLOR)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 + 60))
        screen.blit(instruction_surface, instruction_rect)

    def on_food_eaten(self):
        audio.audio.play_effect('food')

    def on_game_over(self):
        audio.audio.play_effect('game_over')
        audio.audio.stop_music()

# Создание экземпляра игры
main_game = Main()

# Создание события для обновления змейки
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Основной игровой цикл
while True:
    for event in main_game.input.get_events():
        if event.type == "quit":
            pygame.quit()
            sys.exit()
        if event.type == "user" and event.user_type == SCREEN_UPDATE:
            main_game.update()
        if event.type == "key_down":
            key = event.key
            if main_game.settings_active:
                if key == pygame.K_s:
                    main_game.toggle_sound()
                if key == pygame.K_ESCAPE:
                    main_game.settings_active = False
            else:
                if key == pygame.K_SPACE and not main_game.game_active:
                    main_game.start_game()
                elif key == pygame.K_n and not main_game.game_active:
                    main_game.settings_active = True
                if main_game.game_active:
                    if key == pygame.K_UP and main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                    if key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                    if key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                    if key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
    
    screen.fill(BACKGROUND_COLOR)
    main_game.draw_elements()

    if not main_game.game_active:
        if main_game.settings_active:
            main_game.draw_settings()
        else:
            font = pygame.font.Font(None, 74)
            title_surface = font.render('🐍 Змейка', True, SCORE_COLOR)
            title_rect = title_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 - 50))
            screen.blit(title_surface, title_rect)

            font = pygame.font.Font(None, 50)
            instruction_surface = font.render('Нажмите ПРОБЕЛ для начала', True, SCORE_COLOR)
            instruction_rect = instruction_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 + 50))
            screen.blit(instruction_surface, instruction_rect)
            settings_surface = font.render('Нажмите N для настроек', True, SCORE_COLOR)
            settings_rect = settings_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 + 100))
            screen.blit(settings_surface, settings_rect)

    pygame.display.update()
    clock.tick(60)
