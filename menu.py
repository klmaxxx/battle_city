import sys

import pygame

# Константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 50


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
        # screen.blit(
        #     pygame.transform.scale(pygame.image.load("assets/settings_button.png"), (336, 64)),
        #     (250, 400),
        # )

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
                # if event.key == pygame.K_RIGHT:
                #     pygame.mixer.music.set_volume()

        clock.tick(60)
