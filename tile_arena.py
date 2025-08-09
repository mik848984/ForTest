import pygame
from pygame import Rect

# Initialize Pygame
pygame.init()

TILE_SIZE = 32
MAP_WIDTH = 20
MAP_HEIGHT = 15
SCREEN = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
pygame.display.set_caption("Tile Arena Demo")
CLOCK = pygame.time.Clock()

# Generate tile surfaces instead of loading textures
FLOOR_IMG = pygame.Surface((TILE_SIZE, TILE_SIZE))
FLOOR_IMG.fill((170, 170, 170))
FLOOR_IMG = FLOOR_IMG.convert()
WALL_IMG = pygame.Surface((TILE_SIZE, TILE_SIZE))
WALL_IMG.fill((100, 100, 100))
WALL_IMG = WALL_IMG.convert()

# Simple map layout (0=floor, 1=wall)
MAP = [
    [1]*MAP_WIDTH,
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1] + [0]*(MAP_WIDTH-2) + [1],
    [1]*MAP_WIDTH,
]

# Precompute wall rectangles for collision
walls = []
for y, row in enumerate(MAP):
    for x, cell in enumerate(row):
        if cell == 1:
            rect = Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            walls.append(rect)

class Player:
    def __init__(self):
        self.rect = Rect(TILE_SIZE*2, TILE_SIZE*2, TILE_SIZE, TILE_SIZE)
        self.color = (200, 50, 50)
        self.speed = 4

    def move(self, dx, dy):
        # Attempt horizontal move
        if dx:
            self.rect.x += dx
            for wall in walls:
                if self.rect.colliderect(wall):
                    if dx > 0:
                        self.rect.right = wall.left
                    else:
                        self.rect.left = wall.right
        # Attempt vertical move
        if dy:
            self.rect.y += dy
            for wall in walls:
                if self.rect.colliderect(wall):
                    if dy > 0:
                        self.rect.bottom = wall.top
                    else:
                        self.rect.top = wall.bottom

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

player = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx -= player.speed
    if keys[pygame.K_RIGHT]:
        dx += player.speed
    if keys[pygame.K_UP]:
        dy -= player.speed
    if keys[pygame.K_DOWN]:
        dy += player.speed

    player.move(dx, dy)

    # Draw map
    for y, row in enumerate(MAP):
        for x, cell in enumerate(row):
            if cell == 0:
                SCREEN.blit(FLOOR_IMG, (x*TILE_SIZE, y*TILE_SIZE))
            else:
                SCREEN.blit(WALL_IMG, (x*TILE_SIZE, y*TILE_SIZE))

    player.draw(SCREEN)
    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
