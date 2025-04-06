import pygame 

pygame.init()

#tut, dumau, dazhe obyasnyat ne nado
class Enemy:
    def __init__(self, image, x, y, width, height):
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height)).convert_alpha()
        self.x = x  
        self.y = y
    
#otrisovka sprite'a   
    def reset(self, screen, x, y):
        screen.blit(self, (x, y))
    
    def attack(self, p_x, p_y):
        if self.x != p_x - 10 and self.y != p_y - 10:
            while self.x != p_x-10 and self.y != p_y - 10:
                
