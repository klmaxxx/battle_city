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
BLACK = (0, 0, 0)
TILE_SIZE = 40

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

def show_game_over(screen, message, victory=False):
    font = pygame.font.Font(None, 74)
    text_color = (0, 255, 0) if victory else (255, 0, 0)
    text = font.render(message, True, text_color)
    restart_text = pygame.font.Font(None, 36).render(
        "Press enter to restart", True, (255, 255, 255))
    menu_text = pygame.font.Font(None, 36).render(
        "Press Esc to return to menu", True, (255, 255, 255))
    
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
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Рестарт
                elif event.key == pygame.K_ESCAPE:
                    return False  # В меню

def main():
    clock = pygame.time.Clock()
    
    while True:
        # Показ главного меню
        show_menu(screen)
        
        # Показ меню выбора уровня
        selected_level = show_level_menu(screen)
        if selected_level is None:
            pygame.quit()
            return
            
        # Загрузка уровня
        level_data = load_level_map(selected_level)
        if not level_data:
            logging.error(f"Failed to load level {selected_level}")
            continue
            
        walls = build_walls_from_map(level_data)
        free_cells = get_free_cells(level_data)
        
        if not free_cells:
            logging.error("No free cells found in level map")
            continue
            
        # Создание игрока в случайной свободной позиции
        player_x, player_y = free_cells[0]
        player = Player(player_x, player_y)

        # Создание врагов в свободных позициях (не ближе 3 клеток к игроку)
        enemies = pygame.sprite.Group()
        enemy_positions = []

        for cell in free_cells[1:]:
            # Проверяем расстояние до игрока
            dist = ((cell[0] - player_x)**2 + (cell[1] - player_y)**2)**0.5
            if dist > 3 * TILE_SIZE and len(enemies) < 3:
                enemy = Enemy("assets/enemy.png", cell[0], cell[1], TILE_SIZE, TILE_SIZE)
                enemy.walls = walls
                enemies.add(enemy)
                enemy_positions.append(cell)
        
        # Группы спрайтов
        all_sprites = pygame.sprite.Group(player)
        all_sprites.add(*enemies)
        bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        
        logging.info(f"Game started - Level {selected_level}")
        
        # Музыка
        try:
            pygame.mixer.music.load("assets/soundtrack.mp3")
            pygame.mixer.music.play(-1)  # Зацикливание музыки
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
            
            # Обновление стен
            for wall in walls[:]:  # Используем копию списка для безопасного удаления
                wall.update(screen)
                wall.check_collision(bullets)
                wall.player_collide(player)
                if wall.is_destroyed():
                    walls.remove(wall)
            
            # Обновление игрока и пуль
            player.update(keys)
            bullets.update(walls)
            enemy_bullets.update(walls)
            
            # Обновление врагов и их стрельба
            current_time = pygame.time.get_ticks()
            for enemy in enemies:
                enemy.update(screen, player.rect.x, player.rect.y)
                
                # Стреляем не чаще чем раз в 2 секунды
                if current_time - getattr(enemy, 'last_shot_time', 0) > 2000:
                    if enemy.direction == "UP":
                        enemy_bullet = Bullet(enemy.rect.centerx, enemy.rect.top, "UP")
                    elif enemy.direction == "DOWN":
                        enemy_bullet = Bullet(enemy.rect.centerx, enemy.rect.bottom, "DOWN")
                    elif enemy.direction == "LEFT":
                        enemy_bullet = Bullet(enemy.rect.left, enemy.rect.centery, "LEFT")
                    elif enemy.direction == "RIGHT":
                        enemy_bullet = Bullet(enemy.rect.right, enemy.rect.centery, "RIGHT")
                    
                    enemy_bullets.add(enemy_bullet)
                    all_sprites.add(enemy_bullet)
                    enemy.last_shot_time = current_time
            
            # Проверка попаданий пуль игрока во врагов
            for bullet in bullets:
                hit_enemy = pygame.sprite.spritecollide(bullet, enemies, True)
                if hit_enemy:
                    bullet.kill()
            
            # Проверка смерти игрока
            if (pygame.sprite.spritecollideany(player, enemies) or 
                pygame.sprite.spritecollideany(player, enemy_bullets)):
                if show_game_over(screen, "You lost!"):
                    running = False
                    break  # Выход из игрового цикла для рестарта
                else:
                    pygame.quit()
                    return
            
            # Проверка победы
            if not enemies:
                if show_game_over(screen, "You won!", victory=True):
                    running = False
                    break 
                else:
                    pygame.quit()
                    return
            
            # Отрисовка всех спрайтов
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()