import pygame
import random
import math
from bullet import Bullet

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, bullets_group, walls):
        super().__init__()
        self.original_image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.player = player
        self.bullets_group = bullets_group
        self.shoot_cooldown = 0
        self.health = 3
        self.walls = walls

        self.move_timer = 0
        self.player_chase_chance = 0.3  # 30% шанс поехать к игроку

    def update(self):
        self.move()
        self.check_wall_collisions()
        self.try_shoot()
        self.move_timer += 1

        if self.move_timer >= 60:  # каждые 60 кадров (~1 секунда)
            self.decide_direction()
            self.move_timer = 0

    def decide_direction(self):
        if random.random() < self.player_chase_chance:
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            if abs(dx) > abs(dy):
                self.direction = 'RIGHT' if dx > 0 else 'LEFT'
            else:
                self.direction = 'DOWN' if dy > 0 else 'UP'
        else:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

        self.rotate()

    def move(self):
        next_rect = self.rect.copy()

        if self.direction == 'UP':
            next_rect.y -= self.speed
        elif self.direction == 'DOWN':
            next_rect.y += self.speed
        elif self.direction == 'LEFT':
            next_rect.x -= self.speed
        elif self.direction == 'RIGHT':
            next_rect.x += self.speed

        if 0 <= next_rect.left <= SCREEN_WIDTH - next_rect.width and 0 <= next_rect.top <= SCREEN_HEIGHT - next_rect.height:
            self.rect = next_rect
        else:
            self.try_avoid_wall()


    def check_wall_collisions(self):
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.direction == 'UP':
                    self.rect.top = wall.rect.bottom
                elif self.direction == 'DOWN':
                    self.rect.bottom = wall.rect.top
                elif self.direction == 'LEFT':
                    self.rect.left = wall.rect.right
                elif self.direction == 'RIGHT':
                    self.rect.right = wall.rect.left
                self.try_avoid_wall()

    def try_avoid_wall(self):
        options = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        options.remove(self.direction)
        random.shuffle(options)

        for option in options:
            test_rect = self.rect.copy()
            if option == 'UP':
                test_rect.y -= self.speed * 5
            elif option == 'DOWN':
                test_rect.y += self.speed * 5
            elif option == 'LEFT':
                test_rect.x -= self.speed * 5
            elif option == 'RIGHT':
                test_rect.x += self.speed * 5

            if not any(test_rect.colliderect(w.rect) for w in self.walls):
                self.direction = option
                self.rotate()
                break

    def rotate(self):
        if self.direction == 'UP':
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == 'RIGHT':
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == 'DOWN':
            self.image = self.original_image
        elif self.direction == 'LEFT':
            self.image = pygame.transform.rotate(self.original_image, -90)

        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def try_shoot(self):
        if self.shoot_cooldown <= 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.bullets_group.add(bullet)
            self.shoot_cooldown = 10
        else:
            self.shoot_cooldown -= 1
