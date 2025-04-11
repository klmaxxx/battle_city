import pygame
import sys

# Константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50

def show_menu(screen):
    pygame.font.init()
    pygame.mixer.init()
    font = pygame.font.Font(None, FONT_SIZE)
    clock = pygame.time.Clock()
    pygame.mixer.music.load("assets/soundtrack1.mp3")
    pygame.mixer.music.play()

    menu_running = True
    while menu_running:
        screen.fill(BLACK)

        # Отображение текста меню
        title_text = font.render("Battle City Remake", True, WHITE)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        quit_text = font.render("Press ESC to Quit", True, WHITE)

        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 150))
        screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 250))
        screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 350))

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
