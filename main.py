import logging

import pygame

from bullet import Bullet
from player import Player

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

# Карта
wall = pygame.image.load("assets/brick.png")


def main():
    clock = pygame.time.Clock()
    running = True

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()

    logging.info("Game started")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                logging.info("Game exited by user")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()

        screen.fill(BLACK)
        all_sprites.draw(screen)
        screen.blit(wall, (50, 100))
        screen.blit(wall, (250, 100))
        screen.blit(wall, (450, 100))
        screen.blit(wall, (650, 100))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    logging.info("Game loop ended")


if __name__ == "__main__":
    main()
