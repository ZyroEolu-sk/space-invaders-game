import pygame
import os
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, pos, colour, bullet_width, bullet_height, bullet_yvel, bullet_xvel):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(colour)
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.bullet_xvel = bullet_xvel
        self.bullet_yvel = bullet_yvel

    def update(self):
        # La lógica de colisiones la hemos movido al main.py para mantener esto limpio
        self.rect.y += self.bullet_yvel * self.direction
        self.rect.x += self.bullet_xvel * self.direction
        if self.rect.y < -10 or self.rect.y > WINDOW_HEIGHT + 10:
            self.kill()

class Power(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "live.png")), (45, 45))
        self.rect = self.image.get_rect(center = pos)
        
    def update(self):
        self.rect.y += LIVE_VEL
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.explosion_animation_list = []
        explosion_folder = os.path.join(ASSETS_PATH, "animations", "EXPLOSION_2")
        
        # Cargar los 3 frames de la explosión dinámicamente
        for i in range(3):
            img = pygame.transform.scale(pygame.image.load(os.path.join(explosion_folder, f"explosion-animation-frame-{i}.png")), (width, height))
            self.explosion_animation_list.append(img)
            
        self.index = 0
        self.image = self.explosion_animation_list[self.index]
        self.rect = self.image.get_rect(center=[x_pos, y_pos])
        self.counter = 0
    
    def update(self):
        explosion_speed = 6
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.explosion_animation_list) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.explosion_animation_list[self.index]
        
        if self.index >= len(self.explosion_animation_list) - 1 and self.counter >= explosion_speed:
            self.kill()

class TeleportAway(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.anim_list = []
        folder = os.path.join(ASSETS_PATH, "animations", "TELEPORT_AWAY")
        for i in range(13):
            img = pygame.transform.scale(pygame.image.load(os.path.join(folder, f"pixil-frame-{i}.png")), (90, 90))
            self.anim_list.append(img)
        
        self.index = 0
        self.counter = 0
        self.image = self.anim_list[self.index]
        self.rect = self.image.get_rect(center=[x_pos, y_pos])

    def update(self):
        anim_speed = 2
        self.counter += 1
        if self.index >= len(self.anim_list) - 1:
            self.kill()
        elif self.counter >= anim_speed:
            self.index += 1
            self.counter = 0
            self.image = self.anim_list[self.index]

class Teleport(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, game):
        super().__init__()
        self.game = game # Referencia al juego para poder invocar TeleportAway al terminar
        self.anim_list = []
        folder = os.path.join(ASSETS_PATH, "animations", "TELEPORT_AWAY")
        # El teleport normal es la animación al revés (del 12 al 0)
        for i in range(12, -1, -1):
            img = pygame.transform.scale(pygame.image.load(os.path.join(folder, f"pixil-frame-{i}.png")), (90, 90))
            self.anim_list.append(img)
            
        self.index = 0
        self.counter = 0
        self.image = self.anim_list[self.index]
        self.rect = self.image.get_rect(center=[x_pos, y_pos])

    def update(self):
        anim_speed = 2
        self.counter += 1
        if self.index >= len(self.anim_list) - 1:
            ta = TeleportAway(self.rect.x + 45, self.rect.y + 45)
            self.game.teleport_away_group.add(ta)
            self.kill()
        elif self.counter >= anim_speed:
            self.index += 1
            self.counter = 0
            self.image = self.anim_list[self.index]