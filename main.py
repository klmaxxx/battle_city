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

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

# Карта
walls = [Wall(500, 100, 100, 100, "assets/brick.png"), Wall(200, 300, 35, 100, "assets/brick.png")]


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
        enemy1 = Enemy(player, 100, 100, enemy_bullets, walls)
        enemy2 = Enemy(player, 700, 100, enemy_bullets, walls)
        enemy3 = Enemy(player, 400, 300, enemy_bullets, walls)
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
            for wall in walls:
                wall.update(screen)

            player.update(keys)
            bullets.update()
            enemy_bullets.update()

            # Логика врагов
            for enemy in enemies:
                enemy.update(screen, player.rect.x, player.rect.y)
                if pygame.time.get_ticks() % 100 == 0:  # Враги стреляют с интервалом
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

            # Проверка попадания пули во врага
            for bullet in bullets:
                hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
                if hit_enemy:
                    hit_enemy.kill()
                    bullet.kill()

            # Проверка на поражение
            if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(
                player, enemy_bullets
            ):
                all_sprites.empty()  # Удаляем все объекты
                show_game_over(screen, "Поражение")
                running = False

            # Проверка на победу
            if not enemies:
                all_sprites.empty()  # Удаляем все объекты
                show_game_over(screen, "Победа", victory=True)
                running = False

            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

        # Ожидание нажатия Enter для перезапуска или Esc для выхода в меню
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    logging.info("Game exited by user")
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_restart = False  # Перезапуск игры
                    elif event.key == pygame.K_ESCAPE:
                        show_menu(screen)  # Выход в меню
                        waiting_for_restart = False


def show_game_over(screen, message, victory=False):
    font = pygame.font.Font(None, 74)
    text_color = (
        (0, 255, 0) if victory else (255, 0, 0)
    )  # Зеленый для победы, красный для поражения
    text = font.render(message, True, text_color)
    restart_text = pygame.font.Font(None, 36).render(
        "Чтобы переиграть нажмите Enter", True, (255, 255, 255)
    )
    menu_text = pygame.font.Font(None, 36).render(
        "Чтобы выйти в меню нажмите Esc", True, (255, 255, 255)
    )
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
    pygame.time.wait(1000)  # Короткая пауза перед ожиданием ввода


if __name__ == "__main__":
    main()
