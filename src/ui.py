import pygame
from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, text, text_size, width, height, x, y): 
        super().__init__()
        self.rect = pygame.Rect((x, y), (width, height))
        self.frame = pygame.Rect((x-2, y-2), (width + 4, height +4))

        gui_font = pygame.font.SysFont("yugothicmedium", text_size) 
        self.text_surf = gui_font.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.frame)
        pygame.draw.rect(surface, BLACK, self.rect)
        surface.blit(self.text_surf, self.text_rect)