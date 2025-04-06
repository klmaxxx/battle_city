import pygame

PLAYER_SIZE = 40
PLAYER_SPEED = 5
RED = (255, 0, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.direction = 'UP'
        self.speed = PLAYER_SPEED
        self.health = 3
    #движение танка
    def update(self, keys):

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = 'UP'

        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = 'DOWN'

        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = 'LEFT'

        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'RIGHT'
        #ограничение танка
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))

        self.rotate()
    #поворот танка
    def rotate(self):
        if self.direction == 'UP':
            self.image = pygame.transform.rotate(self.image, 0)
        elif self.direction == 'RIGHT':
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.direction == 'DOWN':
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'LEFT':
            self.image = pygame.transform.rotate(self.image, 90)
        #чтобы танк всегда был в определенном направлении
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
