import pygame

PLAYER_SIZE = 40
PLAYER_SPEED = 3
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert_alpha()  
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.direction = None
        self.speed = PLAYER_SPEED
        self.health = 3


    def update(self, keys, walls):
        moving = False  

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = 'UP'
            moving = True
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = 'DOWN'
            moving = True
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = 'LEFT'
            moving = True
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'RIGHT'
            moving = True

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        if moving:
            self.rotate()
        self.check_collisions(walls)

        if not self.can_shoot:
            self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            self.can_shoot = True


    def rotate(self):
        if self.direction == 'UP':
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60)) 
        elif self.direction == 'RIGHT':
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.direction == 'DOWN':
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'LEFT':
            self.image = pygame.image.load("assets/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.image = pygame.transform.rotate(self.image, 90)

        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def check_collisions(self, walls):
        for wall in walls:
            if self.rect.colliderect(wall.rect):  
                if self.direction == 'UP':
                    self.rect.top = wall.rect.bottom
                elif self.direction == 'DOWN':
                    self.rect.bottom = wall.rect.top
                elif self.direction == 'LEFT':
                    self.rect.left = wall.rect.right
                elif self.direction == 'RIGHT':
                    self.rect.right = wall.rect.left
    