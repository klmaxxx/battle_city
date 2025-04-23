import logging
import pygame
from bullet import Bullet
from enemy import Enemy
from mapmanager import load_level_map, build_walls_from_map, get_free_cells
from menu import show_menu, show_level_menu
from player import Player

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Инициализация pygame
pygame.init()
pygame.mixer.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40
BLACK = (0, 0, 0)

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

def show_game_over(screen, message, victory=False):
    try:
        image_path = "assets/win_screen.png" if victory else "assets/lose_screen.png"
        game_over_img = pygame.image.load(image_path).convert()
        game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        logging.error(f"Error loading image: {e}")
        game_over_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_over_img.fill((0, 255, 0) if victory else (255, 0, 0))

    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render("Press Enter to restart", True, (255, 255, 255))
    menu_text = restart_font.render("Press Esc to return to menu", True, (255, 255, 255))

    waiting = True
    while waiting:
        screen.blit(game_over_img, (0, 0))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT - 100))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT - 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

def main():
    clock = pygame.time.Clock()

    while True:
        show_menu(screen)
        selected_level = show_level_menu(screen)
        if selected_level is None:
            pygame.quit()
            return

        level_data = load_level_map(selected_level)
        if not level_data:
            logging.error(f"Failed to load level {selected_level}")
            continue

        walls = build_walls_from_map(level_data)
        free_cells = get_free_cells(level_data)
        if not free_cells:
            logging.error("No free cells found in level map")
            continue

        player_x, player_y = free_cells[0]
        player = Player(player_x, player_y)

        enemies = pygame.sprite.Group()
        enemy_positions = []

        for cell in free_cells[1:]:
            dist = ((cell[0] - player_x)**2 + (cell[1] - player_y)**2)**0.5
            if dist > 5 * TILE_SIZE and len(enemies) < 3:
                too_close = False
                for enemy_pos in enemy_positions:
                    if ((cell[0] - enemy_pos[0])**2 + (cell[1] - enemy_pos[1])**2)**0.5 < 3 * TILE_SIZE:
                        too_close = True
                        break
                if not too_close:
                    enemy = Enemy("assets/enemy.png", cell[0], cell[1], TILE_SIZE, TILE_SIZE)
                    enemy.walls = walls
                    enemies.add(enemy)
                    enemy_positions.append(cell)

        all_sprites = pygame.sprite.Group(player)
        all_sprites.add(*enemies)
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()

        logging.info(f"Game started - Level {selected_level}")

        try:
            pygame.mixer.music.load("assets/soundtrack.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            logging.warning(f"Could not load music: {e}")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            keys = pygame.key.get_pressed()
            screen.fill(BLACK)

            for wall in walls[:]:  
                wall.update(screen)
                wall.check_collision(bullets)
                wall.player_collide(player)
                if wall.is_destroyed():
                    walls.remove(wall)

            player.update(keys, walls)
            bullets.update(walls)
            enemy_bullets.update(walls)

            current_time = pygame.time.get_ticks()
            for enemy in enemies:
                enemy.update(screen, player.rect.x, player.rect.y)
                if current_time - getattr(enemy, 'last_shot_time', 0) > 2000:
                    bullet_dir = enemy.direction
                    bullet_pos = {
                        "UP": (enemy.rect.centerx, enemy.rect.top),
                        "DOWN": (enemy.rect.centerx, enemy.rect.bottom),
                        "LEFT": (enemy.rect.left, enemy.rect.centery),
                        "RIGHT": (enemy.rect.right, enemy.rect.centery)
                    }[bullet_dir]
                    enemy_bullet = Bullet(*bullet_pos, bullet_dir)
                    enemy_bullets.add(enemy_bullet)
                    all_sprites.add(enemy_bullet)
                    enemy.last_shot_time = current_time

            for bullet in bullets:
                hit_enemy = pygame.sprite.spritecollide(bullet, enemies, True)
                if hit_enemy:
                    bullet.kill()

            if (pygame.sprite.spritecollideany(player, enemies) or 
                pygame.sprite.spritecollideany(player, enemy_bullets)):
                if show_game_over(screen, "You lost!", victory=False):
                    running = False
                    break
                else:
                    pygame.quit()
                    return

            if not enemies:
                if show_game_over(screen, "You won!", victory=True):
                    running = False
                    break
                else:
                    pygame.quit()
                    return

            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
