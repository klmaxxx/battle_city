import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path="assets/brick.png"):
        super().__init__()
        try:
            self.image = pygame.transform.scale(
                pygame.image.load(image_path), (width, height))
        except:
            self.image = pygame.Surface((width, height))
            self.image.fill((139, 69, 19))
        self.rect = pygame.Rect(x, y, width, height)
        self.hit_count = 4
        self.collision_rect = pygame.Rect(x, y, width, height)  

        shrink_amount = 1
        self.collision_rect = pygame.Rect(
            x + shrink_amount, 
            y + shrink_amount, 
            width - 2 * shrink_amount, 
            height - 2 * shrink_amount
        )

    def take_damage(self):
        self.hit_count -= 1
        if self.hit_count <= 0:
            self.kill()

    def is_destroyed(self):
        return self.hit_count <= 0

    def update(self, screen):
        if not self.is_destroyed():
            screen.blit(self.image, self.rect)

    def player_collide(self, player):
        if player.rect.colliderect(self.collision_rect):
            # Точное определение стороны столкновения
            if player.direction == 'RIGHT' and player.rect.right > self.rect.left and player.rect.left < self.rect.left:
                player.rect.right = self.rect.left
            elif player.direction == 'LEFT' and player.rect.left < self.rect.right and player.rect.right > self.rect.right:
                player.rect.left = self.rect.right
            elif player.direction == 'DOWN' and player.rect.bottom > self.rect.top and player.rect.top < self.rect.top:
                player.rect.bottom = self.rect.top
            elif player.direction == 'UP' and player.rect.top < self.rect.bottom and player.rect.bottom > self.rect.bottom:
                player.rect.top = self.rect.bottom

    def kill(self):
        self.rect.x = -100
        self.rect.y = -100
        self.collision_rect.x = -100
        self.collision_rect.y = -100

    def check_collision(self, bullets):
        for bullet in bullets:
            if self.collision_rect.colliderect(bullet.rect):
                bullet.kill()
                self.take_damage()


def load_level_map(level):
    if level == 1:
        return [
            "###################",
            "#.....#####.....###",
            "#.###.......###...#",
            "#.#.#.#####.#.#.#.#",
            "#.#.#.#...#.#.#.#.#",
            "#.###.#.#.#.###.#.#",
            "#.....#.#.#.....#.#",
            "#####.#.#.#.#####.#",
            "#.....#.#.#.....#.#",
            "#.###.#.#.#.###.#.#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#.#.#...#.#.#.#.#",
            "#.###.#####.###...#",
            "#.....#####.....###",
            "###################"
        ]
    elif level == 2:
        return [
            "###################",
            "#...#.......#.....#",
            "#.#.#.#####.#.###.#",
            "#.#.#.#...#.#.#...#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#...#.#.#...#.#.#",
            "#.#####.#.#####.#.#",
            "#.......#.......#.#",
            "#.#####.#.#####.#.#",
            "#.#...#.#.#...#.#.#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#.#.....#.#.#...#",
            "#...#.......#.....#",
            "###################"
        ]
    elif level == 3:
        return [
            "###################",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.................#",
            "####.#######.######",
            "#.................#",
            "#.####.....####...#",
            "#.................#",
            "######.#######.####",
            "#.................#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#.#.#.#.#.#.#.#.#",
            "#.#.#.#.#.#.#.#.#.#",
            "###################"
        ]
    else:
        return []

def build_walls_from_map(level_data, brick_image="assets/brick.png", tile_size=40):
    walls = []
    for row_idx, row in enumerate(level_data):
        for col_idx, cell in enumerate(row):
            if cell == "#":
                x = col_idx * tile_size
                y = row_idx * tile_size
                walls.append(Wall(x, y, tile_size, tile_size, brick_image))
    return walls

def get_free_cells(level_data, tile_size=40):
    free_cells = []
    for row_idx, row in enumerate(level_data):
        for col_idx, cell in enumerate(row):
            if cell == ".":
                x = col_idx * tile_size
                y = row_idx * tile_size
                free_cells.append((x, y))
    return free_cells