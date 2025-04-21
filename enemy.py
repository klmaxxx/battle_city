import pygame
import random

pygame.init()

# Класс врага
class Enemy(pygame.sprite.Sprite): 
    def __init__(self, image_path, x, y, width, height):
        super().__init__()  
        self.original_image = pygame.transform.scale(
            pygame.image.load(image_path), (width, height)
        ).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.x = x  
        self.y = y
        self.width = width
        self.height = height
        
        self.direction = "DOWN"  
        self.speed = 1
        self.walls = []
        self.last_shot_time = 0  

    def update(self, screen, target_x, target_y):
        if abs(self.x - target_x) > 0:
            if self.x < target_x:
                self.x += self.speed
                self.direction = "RIGHT"
            elif self.x > target_x:
                self.x -= self.speed
                self.direction = "LEFT"

        elif abs(self.y - target_y) > 0:
            if self.y < target_y:
                self.y += self.speed
                self.direction = "DOWN"
            elif self.y > target_y:
                self.y -= self.speed
                self.direction = "UP"

        self.rect.topleft = (self.x, self.y)

        self.handle_collision()  # Проверка и обработка столкновений

        self.rotate()
        screen.blit(self.image, self.rect)

    def handle_collision(self):
        """Проверяет столкновение с препятствиями и разворачивается в противоположную сторону при столкновении."""
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.change_direction()  # Разворот в противоположную сторону
                return True
        return False

    def change_direction(self):
        """Изменяет направление врага на противоположное и сразу начинает движение."""
        if self.direction == "UP":
            self.direction = "DOWN"
            self.y += self.speed
        elif self.direction == "DOWN":
            self.direction = "UP"
            self.y -= self.speed
        elif self.direction == "LEFT":
            self.direction = "RIGHT"
            self.x += self.speed
        elif self.direction == "RIGHT":
            self.direction = "LEFT"
            self.x -= self.speed
        self.rect.topleft = (self.x, self.y)

    def rotate(self):
        if self.direction == "UP":
            self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == "RIGHT":
            self.image = pygame.transform.rotate(self.original_image, -90)

        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

