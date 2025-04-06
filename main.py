import pygame
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 40
PLAYER_SPEED = 5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))

def main():
    clock = pygame.time.Clock()
    running = True

    # Create player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    logging.info("Game started")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            logging.info("Game exited by user")

    keys = pygame.key.get_pressed()

    all_sprites.update(keys)


    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

    pygame.quit()
    logging.info("Game loop ended")

if name == "__main__":
    main()