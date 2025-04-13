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

    def update(self, screen, target_x, target_y):
        old_x, old_y = self.x, self.y

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

        if self.handle_collision():  # Проверка и обработка столкновений
            self.x, self.y = old_x, old_y  # Возврат к предыдущей позиции
            self.rect.topleft = (self.x, self.y)
            self.try_avoid_wall()  # Попытка сменить направление

        self.rotate()
        screen.blit(self.image, self.rect)

    def handle_collision(self):
        """Проверяет столкновение с препятствиями и возвращает True, если столкновение произошло."""
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                return True
        return False

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

    def try_avoid_wall(self):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        random.shuffle(directions)  # Перемешиваем направления
        for new_direction in directions:
            if self.can_move(new_direction):  # Проверяем возможность движения в новом направлении
                self.direction = new_direction
                if new_direction == "UP":
                    self.y -= self.speed
                elif new_direction == "DOWN":
                    self.y += self.speed
                elif new_direction == "LEFT":
                    self.x -= self.speed
                elif new_direction == "RIGHT":
                    self.x += self.speed
                self.rect.topleft = (self.x, self.y)
                if not self.handle_collision():  # Проверяем, что новое направление свободно
                    break
                else:
                    self.x, self.y = old_x, old_y  # Возврат к предыдущей позиции
                    self.rect.topleft = (self.x, self.y)

    def can_move(self, direction):
        test_rect = self.rect.copy()
        if direction == "UP":
            test_rect.y -= self.speed
        elif direction == "DOWN":
            test_rect.y += self.speed
        elif direction == "LEFT":
            test_rect.x -= self.speed
        elif direction == "RIGHT":
            test_rect.x += self.speed

        for wall in self.walls:
            if test_rect.colliderect(wall.rect):  # Проверка столкновения с новой позицией
                return False
        return True

