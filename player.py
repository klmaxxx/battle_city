import pygame

PLAYER_SIZE = 40
PLAYER_SPEED = 1
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
HITBOX_SHRINK = 10  # На сколько пикселей уменьшаем хитбокс со всех сторон

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/player.png").convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (PLAYER_SIZE, PLAYER_SIZE))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Создаем уменьшенный хитбокс
        self.hitbox = pygame.Rect(
            x + HITBOX_SHRINK,
            y + HITBOX_SHRINK,
            PLAYER_SIZE - 2 * HITBOX_SHRINK,
            PLAYER_SIZE - 2 * HITBOX_SHRINK
        )
        self.direction = 'UP'
        self.speed = PLAYER_SPEED
        self.health = 3
        self.last_position = (x, y)

    def update(self, keys, walls):
        self.last_position = self.rect.topleft
        moved = False

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.hitbox.y -= self.speed
            self.direction = 'UP'
            moved = True
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.hitbox.y += self.speed
            self.direction = 'DOWN'
            moved = True
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.hitbox.x -= self.speed
            self.direction = 'LEFT'
            moved = True
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.hitbox.x += self.speed
            self.direction = 'RIGHT'
            moved = True

        # Проверка столкновений со стенами через хитбокс
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                self.rect.topleft = self.last_position
                self.hitbox.topleft = (
                    self.last_position[0] + HITBOX_SHRINK,
                    self.last_position[1] + HITBOX_SHRINK
                )
                break

        # Ограничение движения по границам экрана с учетом хитбокса
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))
        self.hitbox.x = max(HITBOX_SHRINK, min(self.hitbox.x, SCREEN_WIDTH - PLAYER_SIZE + HITBOX_SHRINK))
        self.hitbox.y = max(HITBOX_SHRINK, min(self.hitbox.y, SCREEN_HEIGHT - PLAYER_SIZE + HITBOX_SHRINK))

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
        # Обновляем позицию хитбокса после вращения
        self.hitbox.center = self.rect.center

    def die(self):
        self.kill()