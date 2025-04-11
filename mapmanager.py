import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))


# класс для стен
class Wall:
    def __init__(self, x, y, width, height, image):
        self.image = pygame.transform.scale(
            pygame.image.load(image), (width, height)
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


img1 = "assets/brick.png"
img2 = "assets/brick1.png"


def map1():
    wall1 = Wall(0, 0, 35, 600, img1)
    wall2 = Wall(300, 100, 35, 100, img1)
    wall3 = Wall(450, 100, 35, 100, img1)
    wall4 = Wall(765, 0, 35, 600, img1)
    wall5 = Wall(235, 200, 100, 35, img2)
    wall6 = Wall(450, 200, 100, 35, img2)
    wall7 = Wall(235, 300, 100, 35, img2)
    wall8 = Wall(450, 300, 100, 35, img2)
    wall9 = Wall(300, 330, 35, 100, img1)
    wall10 = Wall(450, 330, 35, 100, img1)
    wall1.update(screen)
    wall2.update(screen)
    wall3.update(screen)
    wall4.update(screen)
    wall5.update(screen)
    wall6.update(screen)
    wall7.update(screen)
    wall8.update(screen)
    wall9.update(screen)
    wall10.update(screen)


# map = True


# while map:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             map = False
#     screen.fill((0, 0, 0))
#     pygame.display.flip()
