import pygame

PLAYER_SIZE = 60
PLAYER_SPEED = 5
RED = (255, 0, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

#Player class
import pygame

# Константы
PLAYER_SIZE = 40
PLAYER_SPEED = 5
RED = (255, 0, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/player.png").convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (PLAYER_SIZE, PLAYER_SIZE))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.direction = 'UP'
        self.speed = PLAYER_SPEED
        self.health = 3

    def update(self, keys):
        moved = False

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = 'UP'
            moved = True

        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = 'DOWN'
            moved = True

        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = 'LEFT'
            moved = True

        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'RIGHT'
            moved = True

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))

        if moved:
            self.rotate()

    def rotate(self):
        angle = 0
        if self.direction == 'UP':
            angle = 0
        elif self.direction == 'RIGHT':
            angle = -90
        elif self.direction == 'DOWN':
            angle = 180
        elif self.direction == 'LEFT':
            angle = 90

        self.image = pygame.transform.rotate(self.original_image, angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def die(self):
        self.kill()