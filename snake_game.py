import pygame
import random
import sys
from pygame import Vector2
from engine.input import InputManager

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
        self.in_settings = False
        self.input = InputManager()
        self.setting_actions = list(self.input.bindings.keys())
        self.selected_action = 0
        self.waiting_for_key = False
        
    def update(self):
        if self.game_active:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()
    
    def draw_elements(self):
        if self.in_settings:
            self.draw_settings()
        else:
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
    
    def draw_score(self):
        score_text = f'Счёт: {self.score}'
        high_score_text = f'Рекорд: {self.high_score}'
        
        font = pygame.font.Font(None, 50)
        score_surface = font.render(score_text, True, SCORE_COLOR)
        high_score_surface = font.render(high_score_text, True, SCORE_COLOR)
        
        score_x = int(SCREEN_SIZE - 200)
        score_y = int(20)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        
        high_score_x = int(SCREEN_SIZE - 200)
        high_score_y = int(60)
        high_score_rect = high_score_surface.get_rect(center=(high_score_x, high_score_y))
        
        screen.blit(score_surface, score_rect)
        screen.blit(high_score_surface, high_score_rect)

    def draw_settings(self):
        font = pygame.font.Font(None, 60)
        title_surface = font.render('Настройки управления', True, SCORE_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_SIZE/2, 40))
        screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, 40)
        for i, action in enumerate(self.setting_actions):
            mapping = self.input.bindings.get(action, {})
            key_name = mapping.get('keyboard', '')
            key_display = ''
            if key_name and hasattr(pygame, key_name):
                key_display = pygame.key.name(getattr(pygame, key_name)).upper()
            gamepad_display = str(mapping.get('gamepad', '-'))
            text = f"{action}: {key_display} / {gamepad_display}"
            if i == self.selected_action:
                text = '> ' + text
            line_surf = font.render(text, True, SCORE_COLOR)
            screen.blit(line_surf, (40, 100 + i * 40))

        info_surface = font.render('Enter - изменить, Esc - назад', True, SCORE_COLOR)
        info_rect = info_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE - 40))
        screen.blit(info_surface, info_rect)

# Создание экземпляра игры
main_game = Main()

# Создание события для обновления змейки
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        action = main_game.input.get_action(event)

        if main_game.in_settings:
            if main_game.waiting_for_key:
                if event.type == pygame.KEYDOWN:
                    key_name = 'K_' + pygame.key.name(event.key).upper()
                    main_game.input.set_binding(main_game.setting_actions[main_game.selected_action], key_name)
                    main_game.waiting_for_key = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    main_game.input.set_binding(main_game.setting_actions[main_game.selected_action], event.button, 'gamepad')
                    main_game.waiting_for_key = False
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    main_game.in_settings = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    main_game.waiting_for_key = True
                elif action == 'move_up':
                    main_game.selected_action = (main_game.selected_action - 1) % len(main_game.setting_actions)
                elif action == 'move_down':
                    main_game.selected_action = (main_game.selected_action + 1) % len(main_game.setting_actions)
        else:
            if action == 'open_settings' and not main_game.game_active:
                main_game.in_settings = True
            elif action == 'start' and not main_game.game_active:
                main_game.game_active = True
            elif action == 'pause':
                main_game.game_active = not main_game.game_active
            elif main_game.game_active:
                if action == 'move_up' and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if action == 'move_down' and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if action == 'move_left' and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                if action == 'move_right' and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill(BACKGROUND_COLOR)
    main_game.draw_elements()

    if not main_game.game_active and not main_game.in_settings:
        font = pygame.font.Font(None, 74)
        title_surface = font.render('🐍 Змейка', True, SCORE_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 - 50))
        screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, 50)
        instruction_surface = font.render('Нажмите ПРОБЕЛ для начала', True, SCORE_COLOR)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 + 50))
        screen.blit(instruction_surface, instruction_rect)

        font = pygame.font.Font(None, 40)
        settings_surface = font.render('Нажмите S для настроек', True, SCORE_COLOR)
        settings_rect = settings_surface.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2 + 100))
        screen.blit(settings_surface, settings_rect)

    pygame.display.update()
    clock.tick(60)
