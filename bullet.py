import pygame

WHITE = (255, 255, 255)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

pygame.init()
pygame.mixer.init()
shot = pygame.mixer.Sound("assets/shot.mp3")

#Клас пули, для выстрелов
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.direction = direction

    def update(self, walls):
        shot.play()
        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed

        # Проверка столкновения с стенами
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                wall.take_damage()  # Наносим урон стене
                self.kill()  # Уничтожаем пулю
                return

        # Удаление пули при вылете за экран
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()