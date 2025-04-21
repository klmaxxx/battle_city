import sys
import pygame

# Константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
levels_img = pygame.image.load("assets/levels.png")
levels_img = pygame.transform.scale(levels_img, (800, 600))

def show_menu(screen):
    pygame.font.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load("assets/soundtrack1.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()

    menu_running = True
    while menu_running:
        screen.blit(
            pygame.transform.scale(pygame.image.load("assets/main_menu.webp"), (800, 600)), (0, 0)
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER key
                    pygame.mixer.music.pause()
                    menu_running = False
                if event.key == pygame.K_ESCAPE:  # ESC key
                    pygame.quit()
                    sys.exit()

        clock.tick(60)


def show_level_menu(screen):
    pygame.font.init()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)

    level_menu_running = True
    selected_level = 1

    while level_menu_running:
        screen.blit(levels_img, (0, 0))
        
        level1_text = font.render("1. Level 1", True, WHITE if selected_level == 1 else (100, 100, 100))
        level2_text = font.render("2. Level 2", True, WHITE if selected_level == 2 else (100, 100, 100))
        level3_text = font.render("3. Level 3", True, WHITE if selected_level == 3 else (100, 100, 100))

        screen.blit(level1_text, (SCREEN_WIDTH // 2 - level1_text.get_width() // 2, 350))  
        screen.blit(level2_text, (SCREEN_WIDTH // 2 - level2_text.get_width() // 2, 450))  
        screen.blit(level3_text, (SCREEN_WIDTH // 2 - level3_text.get_width() // 2, 550))  

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = max(1, selected_level - 1)
                elif event.key == pygame.K_DOWN:
                    selected_level = min(3, selected_level + 1)
                elif event.key == pygame.K_RETURN:
                    level_menu_running = False
                elif event.key == pygame.K_ESCAPE:
                    level_menu_running = False
                    return None

        clock.tick(60)

    return selected_level