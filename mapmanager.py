import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))


# класс для стен
class Wall:
    def __init__(self, x, y, width, height):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/brick.png"), (width, height)
        ).convert_alpha()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = 100

    # функция для отрисовки стен
    def update(self, screen):
        screen.blit(self.image, (self.x, self.y))

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


wall = Wall(100, 100, 35, 100)
map = True

while map:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            map = False
    screen.fill((0, 0, 0))
    wall.update(screen)
    pygame.display.flip()
