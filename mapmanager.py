import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))


# класс для стен
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.transform.scale(
            pygame.image.load(image_path), (width, height)
        ).convert_alpha()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = 100
        self.hit_count = 4
        self.health = 4  # Здоровье стены

    def take_damage(self):
        """Уменьшает здоровье стены при попадании пули."""
        self.health -= 1

    def is_destroyed(self):
        """Проверяет, разрушена ли стена."""
        return self.health <= 0

    # функция для отрисовки стен
    def update(self, screen):
        if not self.is_destroyed():  # Рисуем стену только если она не разрушена
            screen.blit(self.image, self.rect)

    # функция для коллизий - взял ее из своего старого проекта
    def player_collide(self, player):
        if player.rect.colliderect(self.rect):
            if player.rect.clipline(self.rect.topleft, self.rect.topright):
                # player.rect.y -= player.speedy
                player.rect.bottom = self.rect.top
            if player.rect.clipline(self.rect.bottomleft, self.rect.bottomright):
                # player.rect.y += player.speedy
                player.rect.top = self.rect.bottom
            if player.rect.clipline(self.rect.topright, self.rect.bottomright):
                # player.rect.x += player.speedx
                player.rect.left = self.rect.right
            if player.rect.clipline(self.rect.topleft, self.rect.bottomleft):
                # player.rect.x -= player.speedx
                player.rect.right = self.rect.left

    def kill(self):
        self.x = -100
        self.y = -100
        self.rect.x = -100
        self.rect.y = -100

    def check_collision(self, bullets):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                bullet.kill()  
                self.hit_count -= 1
                if self.hit_count <= 0:
                    self.kill()  


# map = True


# while map:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             map = False
#     screen.fill((0, 0, 0))
#     pygame.display.flip()
