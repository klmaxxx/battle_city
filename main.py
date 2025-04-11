import pygame

from bullet import Bullet
from enemy import Enemy
from mapmanager import Wall, map1
from menu import show_menu
from player import Player

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
    clock = pygame.time.Clock()
    running = True

    show_menu(screen)
    pygame.mixer.music.load("assets/soundtrack.mp3")
    pygame.mixer.music.play()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    enemy = Enemy(100, 100, player, enemy_bullets, walls)
    enemies = pygame.sprite.Group(enemy)
    enemy_bullets = pygame.sprite.Group()
    all_sprites.add(enemy_bullets)
    all_sprites.add(enemy)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.can_shoot:
                        bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                        player.can_shoot = False
                        player.shoot_cooldown = 10

        for bullet in enemy_bullets:
            all_sprites.add(bullet)
            if bullet.rect.colliderect(player.rect):
                bullet.kill()
                player.health -= 1
                print(f"Player health: {player.health}")
                # if player.health <= 0:
                #     pass
                # СДЕЛАЙТЕ ТУТ КОНЕЦ ИГРЫ ТИПО GAME OVER
                #
                #
                #

        for bullet in bullets:
            for wall in walls:
                if bullet.rect.colliderect(wall.rect):
                    bullet.kill()
                    wall.hp -= 25
                    print(f"Wall health: {wall.hp}")
                    if wall.hp <= 0:
                        walls.remove(wall)
                    break

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    enemy.health -= 1
                    print(f"Enemy health: {enemy.health}")
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        all_sprites.remove(enemy)
                    break

        keys = pygame.key.get_pressed()
        player.update(keys, walls)

        bullets.update()
        enemies.update()
        enemy_bullets.update()

        screen.fill(BLACK)

        for wall in walls:
            wall.update(screen)

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
