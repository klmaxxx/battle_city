import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

settings = True

while settings:
    screen.blit(
        pygame.transform.scale(pygame.image.load("assets/main_menu2.png"), (800, 600)), (0, 0)
    )
    screen.blit(
        pygame.transform.scale(pygame.image.load("assets/settings.png"), (600, 500)), (100, 100)
    )
    screen.blit(
        pygame.transform.scale(pygame.image.load("assets/settings_button.png"), (336, 64)),
        (100, 100),
    )
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
