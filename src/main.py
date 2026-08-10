import pygame
import os
import sys
import random
import json

from settings import *
from ui import Button
from effects import Bullet, Explosion, Power, TeleportAway, Teleport
from entities import Aliens, TechAlien, Braincell
from levels import LEVELS, STAR_DIR_DEFAULT

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        
        # Cargar imágenes comunes
        self.font = pygame.font.SysFont(None, 32)
        self.gui_font = pygame.font.Font(None, 50)
        self.myfont = pygame.font.SysFont("colonna", 70) if pygame.font.match_font("colonna") else pygame.font.SysFont(None, 70)
        # La usa draw_game_over(), que se redibuja en cada frame: crearla ahí
        # significaba construir una fuente 60 veces por segundo.
        self.score_font = pygame.font.SysFont("verdana", 20)
        
        self.player_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "sprites", "spaceship_red.png")), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.player_hit_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "sprites", "player_hit_image.png")), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.player_lives_img = pygame.transform.scale(self.player_img, (30, 30))
        
        self.star_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "sprites", "game_screen_star.png")), (20, 20))
        self.score_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "score_image.png")), (250, 250))
        self.live_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "lives_image.png")), (250, 250))
        self.braincell_hit_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "sprites", "BRAINCELL_hit.png")), (400, 400))
        self.hp_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "HP.png")), (350, 350))
        
        self.game_over_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "game_over.png")), (500, 500))
        self.your_score_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "your_score.png")), (250, 250))
        self.highest_score_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "highest_score.png")), (250, 250))
        self.start_bg_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "fondo_inicio.png")), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.press_start_imgs = [
            pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "press_to_start_1.png")), (WINDOW_WIDTH, WINDOW_HEIGHT)),
            pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "ui", "press_to_start_2.png")), (WINDOW_WIDTH, WINDOW_HEIGHT)),
        ]

        # Estrellas de fondo
        self.stars = [{"x": random.randint(0, WINDOW_WIDTH), "y": random.randint(0, WINDOW_HEIGHT)} for _ in range(NUMBER_STARS)]

        # Botones
        self.resume_btn = Button("Resume", 40, 220, 80, 240, 240)
        self.quit_pause_btn = Button("Quit", 40, 220, 70, 240, 370)
        self.retry_btn = Button("Retry", 25, 90, 40, WINDOW_WIDTH/2 - 45, 450)
        self.quit_go_btn = Button("Quit", 25, 90, 40, WINDOW_WIDTH/2 - 45, 530)

        # Configuración inicial del juego
        self.reset_game()

    def reset_game(self):
        # Grupos de Sprites
        self.alien_group = pygame.sprite.Group()
        self.tech_alien_group = pygame.sprite.Group()
        self.braincell_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.live_group = pygame.sprite.Group()
        self.alien_explosions_group = pygame.sprite.Group()
        self.player_explosions_group = pygame.sprite.Group()
        self.lives_explosions_group = pygame.sprite.Group()
        self.teleport_group = pygame.sprite.Group()
        self.teleport_away_group = pygame.sprite.Group()

        # Variables de estado
        self.score = 0
        self.player = pygame.Rect(WINDOW_WIDTH//2-40, 600, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.player_lives = STARTING_LIVES
        self.player_is_alive = True
        self.game_over = False
        self.paused = False
        self.shoot = False
        self.cooldown = 0
        
        # Variables de nivel. El nivel activo es un índice sobre LEVELS, así
        # que añadir uno nuevo no obliga a tocar nada de aquí.
        self.level_index = 0
        self.level_timer = 300
        self.spawn_countdown = 0
        self.waves_spawned = 0

    def save_score(self):
        score_file = os.path.join(BASE_DIR, "score.json")
        highest = 0
        if os.path.exists(score_file):
            with open(score_file, "r") as f:
                try: highest = json.load(f).get("score", 0)
                except: pass
        if self.score > highest:
            with open(score_file, "w") as f:
                json.dump({"score": self.score}, f)
        return max(self.score, highest)

    def create_aliens(self, rows, columns, start_x):
        for col in range(columns):
            for row in range(rows):
                alien = Aliens(start_x + col * 100, -(rows*40) + row * 60)
                self.alien_group.add(alien)

    def boss_create_tech_aliens(self, x, y, number, velocity, possibility):
        for _ in range(number):
            ta = TechAlien(x, y, velocity, possibility)
            self.tech_alien_group.add(ta)

    def handle_collisions(self):
        # Balas contra enemigos
        for bullet in self.bullets_group:
            if bullet.direction == -1: # Bala del jugador
                # Choca con Alien básico
                hits = pygame.sprite.spritecollide(bullet, self.alien_group, True)
                for hit in hits:
                    bullet.kill()
                    self.score += 1
                    exp = Explosion(bullet.rect.x, bullet.rect.y - 33, OVNI_WIDTH, OVNI_HEIGHT)
                    self.alien_explosions_group.add(exp)
                    if hit.red:
                        power = Power((hit.rect.x, hit.rect.y))
                        self.live_group.add(power)
                
                # Choca con TechAlien
                tech_hits = pygame.sprite.spritecollide(bullet, self.tech_alien_group, True)
                for hit in tech_hits:
                    bullet.kill()
                    self.score += 3
                    exp = Explosion(bullet.rect.x, bullet.rect.y - 33, OVNI_WIDTH, OVNI_HEIGHT)
                    self.alien_explosions_group.add(exp)

                # Choca con Braincell
                for boss in self.braincell_group:
                    if boss.rect.colliderect(bullet.rect):
                        boss.lives -= 1
                        bullet.kill()
                        self.screen.blit(self.braincell_hit_img, (boss.rect.x, boss.rect.y))

            elif bullet.direction == 1 and self.player_is_alive: # Bala enemiga
                if self.player.colliderect(bullet.rect):
                    self.player_lives -= 1
                    self.screen.blit(self.player_hit_img, (self.player.x, self.player.y))
                    exp = Explosion(WINDOW_WIDTH - 45 - (3-self.player_lives)*50, 40, 50, 50)
                    self.lives_explosions_group.add(exp)
                    bullet.kill()

        # Enemigos chocando contra el jugador
        if self.player_is_alive:
            for group in [self.alien_group, self.tech_alien_group, self.braincell_group]:
                for enemy in group:
                    if self.player.colliderect(enemy.rect):
                        self.player_lives = 0

            # Power ups: self.player is a Rect, so compare against each sprite rect.
            for power in self.live_group.sprites():
                if self.player.colliderect(power.rect):
                    power.kill()
                    if self.player_lives < 3:
                        self.player_lives += 1
                
        if self.player_lives <= 0 and self.player_is_alive:
            exp = Explosion(self.player.x + 30, self.player.y + 30, PLAYER_WIDTH, PLAYER_HEIGHT)
            self.player_explosions_group.add(exp)
            self.player_is_alive = False
            self.game_over = True

    def draw_bg_and_ui(self):
        star_dx, star_dy = self._get_star_direction_by_level()

        for star in self.stars:
            self.screen.blit(self.star_img, (star["x"], star["y"]))
            star["x"] += star_dx
            star["y"] += star_dy
            self._wrap_star_position(star)

        self.screen.blit(self.score_img, (-70, -90))
        self.screen.blit(self.font.render(str(self.score), True, WHITE), (105, 22))
        self.screen.blit(self.live_img, (360, -90))
        
        lx = WINDOW_WIDTH - 160
        for _ in range(self.player_lives):
            self.screen.blit(self.player_lives_img, (lx, 20))
            lx += 50

    def _get_star_direction_by_level(self):
        """Returns the stars movement vector according to the current level."""
        # draw_bg_and_ui() se dibuja también en pausa, así que sin esto el fondo
        # seguiría desplazándose con el resto del juego congelado.
        if self.paused:
            return 0, 0
        level = self.current_level()
        if level is None:
            return STAR_DIR_DEFAULT
        return level["star_dir"]

    def _wrap_star_position(self, star):
        """Wraps star coordinates when they leave the screen."""
        if star["x"] > WINDOW_WIDTH:
            star["x"] = -20
            star["y"] = random.randint(0, WINDOW_HEIGHT)
        elif star["x"] < -20:
            star["x"] = WINDOW_WIDTH
            star["y"] = random.randint(0, WINDOW_HEIGHT)

        if star["y"] > WINDOW_HEIGHT:
            star["y"] = -20
            star["x"] = random.randint(0, WINDOW_WIDTH)
        elif star["y"] < -20:
            star["y"] = WINDOW_HEIGHT
            star["x"] = random.randint(0, WINDOW_WIDTH)
                    
    def draw_game_over(self):
        high = self.save_score()
        self.screen.fill(BLACK)
        self.screen.blit(self.game_over_img, (WINDOW_WIDTH/2 - 250, -50))
        self.screen.blit(self.your_score_img, (WINDOW_WIDTH/2 - 96, 220))
        self.screen.blit(self.highest_score_img, (WINDOW_WIDTH/2 - 113, 265))
        
        self.screen.blit(self.score_font.render(str(self.score), True, WHITE), (WINDOW_WIDTH/2 + 84, 322))
        self.screen.blit(self.score_font.render(str(high), True, WHITE), (WINDOW_WIDTH/2 + 102, 376))
        
        self.retry_btn.draw(self.screen)
        self.quit_go_btn.draw(self.screen)

    def current_level(self):
        """Nivel activo, o None si ya no queda ninguno (partida ganada)."""
        if 0 <= self.level_index < len(LEVELS):
            return LEVELS[self.level_index]
        return None

    def won(self):
        """True cuando se ha superado el último nivel."""
        return self.level_index >= len(LEVELS)

    def _groups_clear(self, names):
        return all(len(getattr(self, name)) == 0 for name in names)

    def level_manager(self):
        # Lógica centralizada de niveles y oleadas, guiada por la tabla LEVELS.
        level = self.current_level()
        if level is None:
            return

        # Hasta que no se limpie lo que hay en pantalla no se suelta la
        # siguiente oleada ni se avanza de nivel.
        if not self._groups_clear(level["clear_groups"]):
            return

        if level["keep_spawning"](self):
            self.spawn_countdown += 1
            if self.spawn_countdown >= level["spawn_delay"]:
                level["spawn"](self)
                self.level_timer = level["text_timer"]
                self.spawn_countdown = 0
                self.waves_spawned += 1
        else:
            self.level_index += 1
            self.spawn_countdown = 0
            self.waves_spawned = 0

    def run(self):
        # Pantalla de inicio con animación de "press start".
        start_frame = 0
        start_counter = 0
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            start_counter += 1
            if start_counter >= 30:
                start_frame = 1 - start_frame
                start_counter = 0

            self.screen.blit(self.start_bg_img, (0, 0))
            self.screen.blit(self.press_start_imgs[start_frame], (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: waiting = False

        # Bucle de juego
        while True:
            self.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.paused = not self.paused
                    if event.key == pygame.K_SPACE: self.shoot = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE: self.shoot = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.paused:
                        if self.resume_btn.rect.collidepoint(mouse_pos): self.paused = False
                        if self.quit_pause_btn.rect.collidepoint(mouse_pos): pygame.quit(); sys.exit()
                    if self.game_over:
                        if self.retry_btn.rect.collidepoint(mouse_pos): self.reset_game()
                        if self.quit_go_btn.rect.collidepoint(mouse_pos): pygame.quit(); sys.exit()

            # Lógica
            if not self.paused and not self.game_over:
                if self.cooldown > 0: self.cooldown -= 1
                
                # Movimiento del jugador
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT] and self.player.x < WINDOW_WIDTH - 60: self.player.x += PLAYER_VEL
                if keys[pygame.K_LEFT] and self.player.x > 0: self.player.x -= PLAYER_VEL
                
                if self.shoot and self.cooldown == 0 and self.player_is_alive:
                    self.bullets_group.add(Bullet(-1, (self.player.centerx, self.player.y - 15), RED, 5, 17, BULLET_VEL, 0))
                    self.cooldown = 40

                self.level_manager()
                self.handle_collisions()

                # Actualizar grupos
                level = self.current_level()
                if level is not None and level["alien_move"] is not None:
                    self.alien_group.update(self, *level["alien_move"])
                
                self.tech_alien_group.update(self)
                self.braincell_group.update(self)
                self.bullets_group.update()
                self.live_group.update()
                self.alien_explosions_group.update()
                self.player_explosions_group.update()
                self.lives_explosions_group.update()
                self.teleport_group.update()
                self.teleport_away_group.update()

            # Dibujado
            self.screen.fill(BLACK)
            if not self.game_over:
                self.draw_bg_and_ui()
                if self.player_is_alive: self.screen.blit(self.player_img, (self.player.x, self.player.y))
                
                self.alien_group.draw(self.screen)
                self.tech_alien_group.draw(self.screen)
                self.braincell_group.draw(self.screen)
                for boss in self.braincell_group: boss.draw_health(self.screen, self.hp_img)
                self.bullets_group.draw(self.screen)
                self.live_group.draw(self.screen)
                self.alien_explosions_group.draw(self.screen)
                self.player_explosions_group.draw(self.screen)
                self.lives_explosions_group.draw(self.screen)
                self.teleport_group.draw(self.screen)
                self.teleport_away_group.draw(self.screen)
                
                # Textos de nivel
                self.level_timer -= 1
                if 0 < self.level_timer < 260:
                    level = self.current_level()
                    level_label = None
                    if level is not None:
                        primera_oleada = not level.get("label_first_wave_only") or self.waves_spawned == 0
                        if primera_oleada:
                            level_label = level["label"]

                    if level_label is not None:
                        level_text = self.myfont.render(level_label, True, WHITE)
                        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
                        self.screen.blit(level_text, level_rect)
                
                if self.won():
                    win_text = self.myfont.render("YOU WIN!", True, WHITE)
                    win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
                    self.screen.blit(win_text, win_rect)

                if self.paused:
                    self.resume_btn.draw(self.screen)
                    self.quit_pause_btn.draw(self.screen)
            else:
                self.player_explosions_group.draw(self.screen)
                self.player_explosions_group.update()
                if len(self.player_explosions_group) == 0:
                    self.draw_game_over()

            pygame.display.update()

if __name__ == "__main__":
    juego = Game()
    juego.run()