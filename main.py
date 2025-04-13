import logging

import pygame

from bullet import Bullet
from enemy import Enemy
from mapmanager import Wall
from menu import show_menu
from player import Player

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

pygame.init()
pygame.mixer.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
img1 = "assets/brick.png"
img2 = "assets/brick1.png"

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

# Карта
walls = [
    # 1 chast karti
    Wall(500, 100, 35, 100, img1),
    Wall(500, 200, 100, 35, img2),
    Wall(600, 200, 100, 35, img2),
    Wall(700, 200, 100, 35, img2),
    # 2 chast karti
    Wall(100, 100, 35, 100, img1),
    Wall(0, 200, 100, 35, img2),
    Wall(35, 200, 100, 35, img2),
    Wall(650, 230, 35, 100, img1),
    Wall(250, 0, 35, 100, img1),
    Wall(350, 0, 35, 100, img1),
    Wall(350, 100, 35, 100, img1),
    # 3 chast karti
    Wall(0, 400, 100, 35, img2),
    Wall(100, 400, 100, 35, img2),
    Wall(200, 400, 100, 35, img2),
    Wall(300, 400, 100, 35, img2),
    Wall(400, 400, 100, 35, img2),
    Wall(500, 400, 100, 35, img2),
    Wall(600, 400, 100, 35, img2),
    Wall(700, 400, 100, 35, img2),
    Wall(150, 430, 35, 100, img1),
]


def main():
    while True:  # Цикл для перезапуска игры
        clock = pygame.time.Clock()
        running = True

        # Перемещаем игрока подальше от врагов
        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        all_sprites = pygame.sprite.Group(player)
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()

        # Создаем врагов
        enemies = pygame.sprite.Group()
        enemy1 = Enemy("assets/enemy.png", 200, 100, 40, 40)
        enemy2 = Enemy("assets/enemy.png", 700, 100, 40, 40)
        enemy3 = Enemy("assets/enemy.png", 400, 300, 40, 40)
        for enemy in [enemy1, enemy2, enemy3]:
            enemy.walls = walls  # Передаем список стен врагам
        enemies.add(enemy1, enemy2, enemy3)
        all_sprites.add(enemies)

        logging.info("Game started")

        show_menu(screen)
        pygame.mixer.music.load("assets/soundtrack.mp3")
        pygame.mixer.music.play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    logging.info("Game exited by user")
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                        bullets.add(bullet)
                        all_sprites.add(bullet)

            keys = pygame.key.get_pressed()
            screen.fill(BLACK)
            # Карта
            for wall in walls:
                wall.update(screen)
                wall.check_collision(bullets)
                wall.player_collide(player)

            player.update(keys)
            bullets.update()
            enemy_bullets.update()

            for enemy in enemies:
                enemy.update(screen, player.rect.x, player.rect.y)
                if pygame.time.get_ticks() % 100 == 0:
                    if enemy.direction == "UP":
                        enemy_bullet = Bullet(enemy.x + 20, enemy.y, "UP")
                    elif enemy.direction == "DOWN":
                        enemy_bullet = Bullet(enemy.x + 20, enemy.y + 40, "DOWN")
                    elif enemy.direction == "LEFT":
                        enemy_bullet = Bullet(enemy.x, enemy.y + 20, "LEFT")
                    elif enemy.direction == "RIGHT":
                        enemy_bullet = Bullet(enemy.x + 40, enemy.y + 20, "RIGHT")
                    enemy_bullets.add(enemy_bullet)
                    all_sprites.add(enemy_bullet)

            for bullet in bullets:
                hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
                if hit_enemy:
                    hit_enemy.kill()
                    bullet.kill()

            if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(
                player, enemy_bullets
            ):
                all_sprites.empty()
                show_game_over(screen, "You lost!")
                running = False

            # # Проверка на победу
            if not enemies:
                all_sprites.empty()
                show_game_over(screen, "You won!", victory=True)
                running = False

            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    logging.info("Game exited by user")
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_restart = False
                    elif event.key == pygame.K_ESCAPE:
                        show_menu(screen)
                        waiting_for_restart = False


def show_game_over(screen, message, victory=False):
    font = pygame.font.Font(None, 74)
    text_color = (0, 255, 0) if victory else (255, 0, 0)
    text = font.render(message, True, text_color)
    restart_text = pygame.font.Font(None, 36).render(
        "Press enter to get back to restart", True, (255, 255, 255)
    )
    menu_text = pygame.font.Font(None, 36).render("Press Esc to leave", True, (255, 255, 255))
    screen.fill(BLACK)
    screen.blit(
        text,
        (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2),
    )
    screen.blit(
        restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50)
    )
    screen.blit(
        menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100)
    )
    pygame.display.flip()
    pygame.time.wait(1000)


if __name__ == "__main__":
    main()
