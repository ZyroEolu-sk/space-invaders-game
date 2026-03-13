import os, pygame, sys, random, json

#Initiate pygame
pygame.init()

#Initial screen
pygame.display.set_caption("Space Invaders") 
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 650
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#Fotograms Per Second
FPS = 60
FPS_MAIN_MENU = 3
CLOCK = pygame.time.Clock()

#Elements of starting sceen
path = r"./"
STARTING_SCREEN_IMAGE = pygame.image.load(os.path.join(path,"fondo_inicio.png"))
STARTING_SCEEN = pygame.transform.scale(STARTING_SCREEN_IMAGE,(WINDOW_HEIGHT,WINDOW_WIDTH))
PRESS_TO_START_1_IMAGE = pygame.image.load(os.path.join(path,"press_to_start_1.png"))
PRESS_TO_START_1 = pygame.transform.scale(PRESS_TO_START_1_IMAGE,(WINDOW_WIDTH,WINDOW_HEIGHT))
PRESS_TO_START_2_IMAGE = pygame.image.load(os.path.join(path,"press_to_start_2.png"))
PRESS_TO_START_2 = pygame.transform.scale(PRESS_TO_START_2_IMAGE,(WINDOW_WIDTH,WINDOW_HEIGHT))
change_time = 1

#Elements of game screen

#Score
font = pygame.font.SysFont(None, 32)
score = 0

#Stars
STAR_WIDTH, STAR_HEIGHT = 1, 1
STAR_IMAGE = pygame.image.load(os.path.join(path,"game_screen_star.png"))
STAR = pygame.transform.scale(STAR_IMAGE,(STAR_WIDTH, STAR_HEIGHT))
star_list = []
star_x = []
star_y = []
NUMBER_STARS = 10
STAR_VEL = 6

#Paused game
paused_game = False
RS_WIDTH = 220
RS_HEIGHT = 80
RS_X = 240
RS_Y = 240
Q_WIDTH = 220
Q_HEIGHT = 70
Q_X = 240
Q_Y = 370

#Game over
RGO_WIDTH =90
RGO_HEIGHT =40
RGO_X = WINDOW_WIDTH/2 - RGO_WIDTH/2
RGO_Y =450

QGO_WIDTH =90
QGO_HEIGHT =40
QGO_X = WINDOW_WIDTH/2 - RGO_WIDTH/2
QGO_Y =530

GAME_OVER_IMAGE = pygame.image.load(os.path.join(path, "game_over.png"))
GAME_OVER = pygame.transform.scale(GAME_OVER_IMAGE, (500, 500))
YOUR_SCORE_IMAGE = pygame.image.load(os.path.join(path, "your_score.png"))
YOUR_SCORE = pygame.transform.scale(YOUR_SCORE_IMAGE, (250, 250))
HIGHEST_SCORE_IMAGE = pygame.image.load(os.path.join(path, "highest_score.png"))
HIGHEST_SCORE = pygame.transform.scale(HIGHEST_SCORE_IMAGE, (250, 250))

#Alien ovni
OVNI_WIDTH, OVNI_HEIGHT = 80, 80
OVNI_VEL_X = 3
OVNI_VEL_Y = 20
columns = 5
rows = 4

#Braincell
BRAINCELL_HIT_IMAGE = pygame.image.load(os.path.join(path,"BRAINCELL_hit.png"))
BRAINCELL_HIT = pygame.transform.scale(BRAINCELL_HIT_IMAGE,(400,400))
HP_IMAGE = pygame.image.load(os.path.join(path,"HP.png"))
HP = pygame.transform.scale(HP_IMAGE,(350, 350))

#Player spaceship
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60
PLAYER_IMAGE = pygame.image.load(os.path.join(path, "spaceship_red.png"))
PLAYER = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_HIT_IMAGE = pygame.image.load(os.path.join(path, "player_hit_image.png"))
PLAYER_HIT = pygame.transform.scale(PLAYER_HIT_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = pygame.Rect(WINDOW_WIDTH//2-40, 600, PLAYER_WIDTH, PLAYER_HEIGHT)
PLAYER_VEL = 8
player_lives = 3
player_is_alive = True
PLAYER_LIVES_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (30, 30))
LIVE_IMAGE = pygame.image.load(os.path.join(path, "lives_image.png"))
LIVE = pygame.transform.scale(LIVE_IMAGE, (250, 250))
lives_explosion_xposition = WINDOW_WIDTH - 45
lives_explosion_yposition = 40
SCORE_IMAGE = pygame.image.load(os.path.join(path, "score_image.png"))
SCORE = pygame.transform.scale(SCORE_IMAGE, (250, 250))
countdown = 0
alien_countdown = 0

#Colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (8, 255, 8)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#levels
myfont = pygame.font.SysFont("colonna", 70)
text_level_1 = myfont.render("LEVEL 1", True, WHITE)
text_level_2 = myfont.render("LEVEL 2", True, WHITE)
text_level_3 = myfont.render("LEVEL 3", True, WHITE)
text_level_4 = myfont.render("LEVEL 4", True, WHITE)
times_placed_level_1 = 0
level_timer = 300
level_1_text_starter = False
level_2_text_starter = False
level_3_text_starter = False
level_4_text_starter = False
level_1 = True
level_2 = False
level_3 = False
level_4 = False

#Bullets
gui_font = pygame.font.Font(None, 50)
BULLET_VEL = 6
bullet_list = []
shoots = []
shoot = False
cooldown = 0

#lives
LIVE_VEL = 1
live_power = False

#Classes
class Button(pygame.sprite.Sprite):
    def __init__(self, text, text_size, width, height, x, y): 
        super().__init__() #Inherits from Sprite class
        self.rect = pygame.Rect((x, y), (width, height))
        self.frame = pygame.Rect((x-2, y-2), (width + 4, height +4))
 
        gui_font = pygame.font.SysFont("yugothicmedium", text_size)
        self.text_surf = gui_font.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

    def draw(self):
        pygame.draw.rect(WINDOW, WHITE, self.frame)
        pygame.draw.rect(WINDOW, BLACK, self.rect)
        WINDOW.blit(self.text_surf, self.text_rect)
        

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #Inherits from Sprite class
        if random.randint(1, 4) > 1:
            self.image = pygame.transform.scale((pygame.image.load(os.path.join(path, "ovni.png"))), (OVNI_WIDTH, OVNI_HEIGHT))
            self.red = False
        else:
            self.image = pygame.transform.scale((pygame.image.load(os.path.join(path, "healer_ovni.png"))), (OVNI_WIDTH, OVNI_HEIGHT))
            self.red = True
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1


    def update(self, distance, possibility, speed):
        self.rect.x += speed * self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > distance:
            self.rect.y += OVNI_VEL_Y
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        if random.randint(3, possibility) == 3:
            shoot_bullets(1, self.rect, GREEN)


class TechAlien(pygame.sprite.Sprite):
    def __init__(self, TECHALIEN_XPOSITION, TECHALIEN_YPOSITION, velocity, possibility):
        pygame.sprite.Sprite.__init__(self)
        self.tech_alien_animation_list = []
        tech_alien_folder = os.path.join(path, "TECH_ALIEN")
        tech_alien_folder_list = os.listdir(os.path.join(path, "TECH_ALIEN"))
        for frame in tech_alien_folder_list:
            tech_alien_frame = pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, frame)),(90, 90))
            self.tech_alien_animation_list.append(tech_alien_frame)
        self.velocity = velocity
        self.possibility = possibility
        self.index = 0
        self.lives = 3
        self.counter = 0
        self.image = self.tech_alien_animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [TECHALIEN_XPOSITION, TECHALIEN_YPOSITION]
        self.direction = 1
    
    def update(self):
        #Animation 
        animation_speed = 3
        self.counter += 1
        
        if self.index >= len(self.tech_alien_animation_list) - 1:
            self.index = 0

        if self.index <= len(self.tech_alien_animation_list) - 1 and self.counter >= animation_speed:
            self.index += 1
            self.counter = 0
            self.image = self.tech_alien_animation_list[self.index] 

        #Behaviour
        if self.rect.y >= 570:
            teleport_away(self.rect.x + 45, self.rect.y + 27)
            self.rect.y = random.randint(-300, 400)
            self.rect.x = random.randint(-50, 450)
            teleport(self.rect.x + 45, self.rect.y + 90)

        if self.rect.y <= -100:
            teleport_away(self.rect.x + 45, self.rect.y + 27)
            self.rect.y = random.randint(-300, 400)
            self.rect.x = random.randint(-50, 450) 
            teleport(self.rect.x + 45, self.rect.y + 90)

        if random.randint(3, self.possibility) == 3:
            shoot_tech_alien_bullets(1, self.rect, BLUE)

        self.rect.y += self.velocity * self.direction


class Braincell(pygame.sprite.Sprite):
    def __init__(self, BRAINCELL_XPOSITION, BRAINCELL_YPOSITION, velocity):
        pygame.sprite.Sprite.__init__(self)
        #Loading base_form images
        self.braincell_animation_list = []
        braincell_folder = os.path.join(path, "BRAINCELL")
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-0.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-1.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-2.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-3.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-4.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-5.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-6.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-7.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-8.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-9.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-10.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-11.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-12.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-13.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-14.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-15.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-16.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-17.png")),(400, 400)))
        self.braincell_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder, "pixil-frame-18.png")),(400, 400)))

        #Loading super_form images
        self.braincell_animation_list_2 = []
        braincell_folder_2 = os.path.join(path, "BRAINCELL_2")
        #self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-0.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-1.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-2.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-3.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-4.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-5.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-6.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-7.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-8.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-9.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-10.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-11.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-12.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-13.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-14.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-15.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-16.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-17.png")),(400, 400)))
        self.braincell_animation_list_2.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_2, "pixil-frame-18.png")),(400, 400)))

        #Load transformation animation
        self.transformation_animation_list = []
        braincell_folder_3 = os.path.join(path, "BRAINCELL_TRANSFORMATION")
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-0.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-1.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-2.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-3.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-4.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-5.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-6.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-7.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-8.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-9.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-10.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-11.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-12.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-13.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-14.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-15.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-16.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-17.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-18.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-19.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-20.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-21.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-22.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-23.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-24.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-25.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-26.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-27.png")),(400, 400)))
        self.transformation_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(braincell_folder_3, "pixil-frame-28.png")),(400, 400)))

        #General elements
        self.velocity = velocity
        self.index = 0
        self.lives = 100
        self.counter = 0
        self.image = self.braincell_animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [BRAINCELL_XPOSITION, BRAINCELL_YPOSITION]
        self.direction = 1

        #Attack patterns
        self.pattern_0 = True
        self.pattern_1 = False
        self.pattern_1_counter = 0
        self.pattern_2 = False
        self.pattern_2_counter = 0
        self.pattern_3 = False
        self.pattern_4 = False
        self.pattern_4_counter = 0
        self.pattern_5 = False

        #health bar and forms
        self.health_bar_width = 0
        self.base_form = True
        self.super_form = False
        self.transformation = False

    def update(self):
        #base_form animation
        if self.base_form == True: 
            animation_speed = 3
            self.counter += 1

            if self.index >= len(self.braincell_animation_list) - 1:
                self.index = 0

            if self.index <= len(self.braincell_animation_list) - 1 and self.counter >= animation_speed:
                self.index += 1
                self.counter = 0
                self.image = self.braincell_animation_list[self.index]
        
        #super_form animation
        elif self.super_form == True:
            animation_speed = 2
            self.counter += 1
            #Animation_2
            if self.index >= len(self.braincell_animation_list_2) - 1:
                self.index = 0

            
            if self.index <= len(self.braincell_animation_list_2) - 1 and self.counter >= animation_speed:
                self.index += 1
                self.counter = 0
                self.image = self.braincell_animation_list_2[self.index]
                
        #transformation animation
        elif self.transformation == True:
            self.rect.x += 0
            self.rect.y += 0
            animation_speed = 2
            self.counter += 1
            #Animation_2
            if self.index >= len(self.transformation_animation_list) - 1:
                self.index = 0
                self.transformation = False
                self.super_form = True

            if self.index <= len(self.transformation_animation_list) - 1 and self.counter >= animation_speed:
                self.index += 1
                self.counter = 0
                self.image = self.transformation_animation_list[self.index]

        #draw health bar
        self.health_bar_width = self.lives * 2
        pygame.draw.rect(WINDOW, GREEN, (self.rect.x + 105, self.rect.y + 310, self.health_bar_width, 10))
        pygame.draw.rect(WINDOW, WHITE, (self.rect.x + 105, self.rect.y + 310, 200, 12), 2)
        WINDOW.blit(HP, (self.rect.x - 90, self.rect.y + 142))

        #Pattern_0 or initial movement
        if self.pattern_0 == True:
            if not self.rect.y >= 100:
                self.rect.y += 1

            elif self.rect.y >= 100:
                self.pattern_0 = False
                self.pattern_1 = True

        #Iniciate combat 
        else:
            #Bullets and hit handle
            for bullet in bullets_group:
                if bullet.direction == -1:
                    if self.rect.colliderect(bullet.rect):
                            self.lives -= 1
                            bullet.kill()
                            WINDOW.blit(BRAINCELL_HIT, (self.rect.x, self.rect.y))

            #Collition wiht player
            global player_lives
            if player.colliderect(self.rect):
                player_lives = 0

            #Death
            if self.lives <= 0:
                self.kill()

            #Base form
            if self.base_form == True:
                #Pattern_1 (goes from one side to another)
                if self.pattern_1 == True:
                    self.rect.y += 0
                    self.rect.x += self.velocity * self.direction
                    if self.rect.x >= 450 or self.rect.x <= -100:
                        self.direction *= -1
                        create_aliens(1, 1, 200)
                        self.pattern_1_counter += 1
                    
                    if random.randint(1, 1300) == 1:
                        self.pattern_1 = False
                        self.pattern_4 = True

                    if self.pattern_1_counter >= 6:
                        self.pattern_1 = False
                        self.pattern_1_counter = 0
                        if random.randint(1,2) == 1:
                            self.pattern_2 = True
                        else:
                            self.pattern_5 = True

                    if random.randint(3, 60) == 3:
                        shoot_braincell_bullets(1, self.rect, WHITE)
                
                #Pattern_2 (goes to the upper part and creates tech aliens)
                if self.pattern_2 == True:
                    self.rect.x += 0
                    if self.rect.y > -50:
                        self.rect.y -= 4
                    if self.rect.y <= -50:
                        if self.rect.x < 400:
                            self.rect.x += 4
                            self.pattern_2_counter += 1
                            if self.pattern_2_counter >= 30: 
                                boss_create_tech_aliens(self.rect.x + 215, self.rect.y + 170, 1, 3, 50)
                                self.pattern_2_counter = 0

                        if self.rect.x >= 400:
                            self.pattern_2 = False
                            self.pattern_3 = True

                #Pattern 3 (goes down)
                if self.pattern_3 == True:
                    if self.rect.y < 100:
                        self.rect.y += 4

                    elif self.rect.y >= 100:
                        self.pattern_3 = False
                        self.pattern_1 = True

                #Pattern 4 (charges down)
                if self.pattern_4 == True:
                    self.rect.x += 0
                    self.pattern_4_counter += 1
                    if self.pattern_4_counter >= 60:
                        self.rect.y += 20
                    if self.rect.y >= 600:
                        self.rect.y = -200
                        self.pattern_3 = True
                        self.pattern_4 = False
                        self.pattern_4_counter = 0
                
                #Pattern 5 (goes to the upper part and makes a bullet rain)
                if self.pattern_5 == True:
                    self.rect.x += 0
                    if self.rect.y > -50:
                        self.rect.y -= 4
                    if self.rect.y <= -50:
                        if self.rect.x < 400:
                            self.rect.x += 4
                            if random.randint(3, 5) == 3:
                                shoot_braincell_bullets(1, self.rect, WHITE)
                            self.pattern_2_counter = 0

                        if self.rect.x >= 400:
                            self.pattern_5 = False
                            self.pattern_3 = True
                
                #Transformation conditions for super form
                if self.lives <= 33:
                    self.base_form = False
                    self.transformation = True
            
            #Super form (same patterns as base form)
            if self.super_form == True:
                if self.pattern_1 == True:
                    self.rect.y += 0
                    self.rect.x += 10 * self.direction
                    if self.rect.x >= 450 or self.rect.x <= -100:
                        self.direction *= -1
                        create_aliens(1, 1, 200)
                        self.pattern_1_counter += 1
                    
                    if random.randint(1, 900) == 1:
                        self.pattern_1 = False
                        self.pattern_4 = True

                    if self.pattern_1_counter >= 4 or self.pattern_1_counter >= 4 and self.rect.x >= 450:
                        self.pattern_1 = False
                        self.pattern_1_counter = 0
                        if random.randint(1,2) == 1:
                            self.pattern_2 = True
                        else:
                            self.pattern_5 = True

                    if random.randint(3, 30) == 3:
                        shoot_braincell_bullets(1, self.rect, WHITE)
                
                if self.pattern_2 == True:
                    self.rect.x += 0
                    if self.rect.y > -50:
                        self.rect.y -= 10
                    if self.rect.y <= -50:
                        if self.rect.x < 400:
                            self.rect.x += 10
                            self.pattern_2_counter += 1
                            if self.pattern_2_counter >= 15: 
                                boss_create_tech_aliens(self.rect.x + 215, self.rect.y + 170, 1, 6, 50)
                                self.pattern_2_counter = 0

                        if self.rect.x >= 400:
                            self.pattern_2 = False
                            self.pattern_3 = True

                if self.pattern_3 == True:
                    if self.rect.y < 100:
                        self.rect.y += 10

                    elif self.rect.y >= 100:
                        self.pattern_3 = False
                        self.pattern_1 = True

                if self.pattern_4 == True:
                    self.rect.x += 0
                    self.pattern_4_counter += 1
                    if self.pattern_4_counter >= 60:
                        self.rect.y += 20
                    if self.rect.y >= 600:
                        self.rect.y = -200
                        self.pattern_3 = True
                        self.pattern_4 = False
                        self.pattern_4_counter = 0

                if self.pattern_5 == True:
                    self.rect.x += 0
                    if self.rect.y > -50:
                        self.rect.y -= 10
                    if self.rect.y <= -50:
                        if self.rect.x < 400:
                            self.rect.x += 10
                            if random.randint(3, 4) == 3:
                                shoot_braincell_bullets(1, self.rect, WHITE)
                            self.pattern_2_counter = 0

                        if self.rect.x >= 400:
                            self.pattern_5 = False
                            self.pattern_3 = True
                

class Bullet(pygame.sprite.Sprite):
    def __init__(self,direction, pos, colour, bullet_width, bullet_height, bullet_yvel, bullet_xvel):
        super().__init__() #Inherits from Sprite class
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(colour)
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.bullet_xvel = bullet_xvel
        self.bullet_yvel = bullet_yvel

    def update(self):
        global score, player_lives, live_power
        self.rect.y +=  self.bullet_yvel* self.direction
        self.rect.x += self.bullet_xvel* self.direction
        if self.rect.y < -10:
            self.kill()
        if self.direction == -1:
            for alien in alien_group:
                for bullet in bullets_group:
                    if bullet.direction == -1:
                        if alien.rect.colliderect(bullet.rect):
                            if alien.red == True:
                                live_power = True
                                live = Power((alien.rect.x, alien.rect.y ))
                                live_group.add(live)
                                score += 1
                                alien_explosion = Explosion(self.rect.x, self.rect.y - 33, OVNI_WIDTH, OVNI_HEIGHT)
                                alien_explosions_group.add(alien_explosion)
                                self.kill()
                                alien.kill()
                                
                            else:
                                score += 1
                                alien_explosion = Explosion(self.rect.x, self.rect.y - 33, OVNI_WIDTH, OVNI_HEIGHT)
                                alien_explosions_group.add(alien_explosion)
                                self.kill()
                                alien.kill()

            for tech_alien in tech_alien_group:
                for bullet in bullets_group:
                    if bullet.direction == -1:
                        if tech_alien.rect.colliderect(bullet.rect):
                                score += 3
                                alien_explosion = Explosion(self.rect.x, self.rect.y - 33, OVNI_WIDTH, OVNI_HEIGHT)
                                alien_explosions_group.add(alien_explosion)
                                self.kill()
                                tech_alien.kill()


class Power(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(path, "live.png")), (45, 45))
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.y += LIVE_VEL
        if self.rect.top > 650:
            self.kill
    

class Explosion(pygame.sprite.Sprite):
    def __init__(self, EXPLOSION_XPOSITION, EXPLOSION_YPOSITION, EXPLOSION_WIDTH, EXPLOSION_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.explosion_animation_list = []

        #Import all the explosion frames
        explosion_folder = os.path.join(path, "EXPLOSION_2")
        explosion_folder_list = os.listdir(explosion_folder)
        for file in explosion_folder_list:
            explosion_image = pygame.transform.scale(pygame.image.load(os.path.join(explosion_folder, file)),
            (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))
            self.explosion_animation_list.append(explosion_image)
            
        self.index = 0
        self.image = self.explosion_animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [EXPLOSION_XPOSITION, EXPLOSION_YPOSITION]
        self.counter = 0
        self.xposition = EXPLOSION_XPOSITION
        self.yposition = EXPLOSION_YPOSITION
    
    def update(self):
        explosion_speed = 6
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.explosion_animation_list) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.explosion_animation_list[self.index]
        
        if self.index >= len(self.explosion_animation_list) - 1 and self.counter >= explosion_speed:
            self.index = 0
            self.kill()


class TeleportAway(pygame.sprite.Sprite):
    def __init__(self, TELEPORTAWAY_XPOSITION, TELEPORTAWAY_YPOSITION):
        pygame.sprite.Sprite.__init__(self)
        self.teleport_away_animation_list = []
        tech_alien_folder = os.path.join(path, "TELEPORT_AWAY")

        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-0.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-1.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-2.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-3.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-4.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-5.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-6.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-7.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-8.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-9.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-10.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-11.png")),(90, 90)))
        self.teleport_away_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-12.png")),(90, 90)))
        self.index = 0
        self.counter = 0
        self.image = self.teleport_away_animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [TELEPORTAWAY_XPOSITION, TELEPORTAWAY_YPOSITION]


    def update(self):
        animation_speed = 2
        self.counter += 1

        if self.index >= len(self.teleport_away_animation_list) - 1:
            self.kill()

        if self.index <= len(self.teleport_away_animation_list) - 1 and self.counter >= animation_speed:
            self.index += 1
            self.counter = 0
            self.image = self.teleport_away_animation_list[self.index] 


class Teleport(pygame.sprite.Sprite):
    def __init__(self, TELEPORT_XPOSITION, TELEPORT_YPOSITION):
        pygame.sprite.Sprite.__init__(self)
        self.teleport_animation_list = []
        tech_alien_folder = os.path.join(path, "TELEPORT_AWAY")

        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-12.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-11.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-10.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-9.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-8.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-7.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-6.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-5.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-4.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-3.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-2.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-1.png")),(90, 90)))
        self.teleport_animation_list.append(pygame.transform.scale(pygame.image.load(os.path.join(tech_alien_folder, "pixil-frame-0.png")),(90, 90)))
        self.index = 0
        self.counter = 0
        self.image = self.teleport_animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [TELEPORT_XPOSITION, TELEPORT_YPOSITION]


    def update(self):
        animation_speed = 2
        self.counter += 1

        if self.index >= len(self.teleport_animation_list) - 1:
            teleport_away(self.rect.x + 45, self.rect.y + 45)
            self.kill()

        if self.index <= len(self.teleport_animation_list) - 1 and self.counter >= animation_speed:
            self.index += 1
            self.counter = 0
            self.image = self.teleport_animation_list[self.index] 


#Sprite groups

#Enemies groups
alien_group = pygame.sprite.Group()
tech_alien_group = pygame.sprite.Group()
braincell_group = pygame.sprite.Group()

#Other secundary elements
teleport_away_group = pygame.sprite.Group()
teleport_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
live_group = pygame.sprite.Group()



#Buttons groups
button_group = pygame.sprite.Group()
resume_pause_button = Button("Resume", 40, RS_WIDTH, RS_HEIGHT, RS_X, RS_Y)
quit_pause_button = Button("Quit", 40, Q_WIDTH, Q_HEIGHT, Q_X, Q_Y)
retry_game_over_button = Button("Retry", 25, RGO_WIDTH, RGO_HEIGHT, RGO_X, RGO_Y)
quit_game_over_button = Button("Quit", 25, QGO_WIDTH, QGO_HEIGHT, QGO_X, QGO_Y)

#Explosions
player_explosions_group = pygame.sprite.Group()
lives_explosions_group = pygame.sprite.Group()
alien_explosions_group = pygame.sprite.Group()


#Game screen functions
def shoot_bullets(direction, subject, colour):
    global cooldown
    if subject == player:
        if cooldown == 0:
            bullet = Bullet(direction, (subject.x + PLAYER_WIDTH//2 - 2, subject.y + PLAYER_HEIGHT//2 - 15), colour, 5, 17, BULLET_VEL, 0)
            bullets_group.add(bullet)
            cooldown = 40
    else:
        bullet = Bullet(direction, (subject.x + PLAYER_WIDTH//2 - 2, subject.y + PLAYER_HEIGHT//2 - 15), colour, 5, 17, BULLET_VEL, 0)
        bullets_group.add(bullet)


def shoot_tech_alien_bullets(direction, subject, colour):
        bullet = Bullet(direction, (subject.x + 45, subject.y + 30), colour, 20, 10, 8, random.randint(-4, 10))
        bullets_group.add(bullet)


def shoot_braincell_bullets(direction, subject, colour):
        bullet = Bullet(direction, (subject.x + 180, subject.y + 150), colour, 20, 20, 8, random.randint(-6, 6))
        bullets_group.add(bullet)


def create_aliens(rows, columns, alien_initial_x):
    for column in range(columns):
        for item in range(rows):
            alien = Aliens(alien_initial_x + column * 100, -(rows*40) + item * 60)
            alien_group.add(alien)


def create_tech_aliens(number_of_aliens, velocity, possibility):
    for _ in range(number_of_aliens):
        tech_alien = TechAlien(random.randint(0, 800), random.randint(-50, 100), velocity, possibility)
        tech_alien_group.add(tech_alien)

def boss_create_tech_aliens(techalien_xposition, techalien_yposition, number_of_aliens, velocity, possibility):
    for _ in range(number_of_aliens):
        tech_alien = TechAlien(techalien_xposition, techalien_yposition, velocity, possibility)
        tech_alien_group.add(tech_alien)

def create_braincell(BRAINCELL_XPOSITION, BRAINCELL_YPOSITION, velocity):
    braincell = Braincell(BRAINCELL_XPOSITION, BRAINCELL_YPOSITION, velocity)
    braincell_group.add(braincell)


def teleport_away(xposition, yposition):
    teleport = TeleportAway(xposition, yposition)
    teleport_away_group.add(teleport)


def teleport(xposition, yposition):
    teleport = Teleport(xposition, yposition)
    teleport_group.add(teleport)
            

def draw_stars():
    for _ in range(NUMBER_STARS):
        STAR_WIDTH, STAR_HEIGHT = 20, 20
        STAR_IMAGE = pygame.image.load(os.path.join(path,"game_screen_star.png"))
        star_list.append(pygame.transform.scale(STAR_IMAGE,(STAR_WIDTH, STAR_HEIGHT)))
        star_x.append(random.randint(0, WINDOW_WIDTH))
        star_y.append(random.randint(0, WINDOW_HEIGHT))

    for x in range(NUMBER_STARS):
        WINDOW.blit(star_list[x],(star_x[x], star_y[x]))
        star_y[x] += STAR_VEL
        if star_y[x] >= WINDOW_HEIGHT:
            star_y[x] = -10
            star_x[x] = random.randint(0, WINDOW_WIDTH)


def player_handle():
    #Right

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_RIGHT] and player.x < WINDOW_WIDTH - 60:
        player.x += PLAYER_VEL
    #Left
    if key_pressed[pygame.K_LEFT] and player.x > 0:
        player.x -= PLAYER_VEL
    #Player collide aliens
    global player_lives, player_is_alive, lives_explosion_xposition, lives_explosion_yposition, game_over
    if player_is_alive:
        if player_lives <= 0:
            player_explosion = Explosion(player.x + 30, player.y + 30, PLAYER_WIDTH, PLAYER_HEIGHT)
            player_explosions_group.add(player_explosion) 
            player_is_alive = False
            game_over = True
            
        else:
            for alien in alien_group:
                if player.colliderect(alien.rect):
                    player_lives = 0
            for tech_alien in tech_alien_group:
                if player.colliderect(tech_alien.rect):
                    player_lives = 0
            for bullet in bullets_group:
                if bullet.direction == 1:       
                    if player.colliderect(bullet.rect):
                        player_lives -= 1
                        WINDOW.blit(PLAYER_HIT, (player.x, player.y))
                        lives_explosion = Explosion(lives_explosion_xposition, lives_explosion_yposition, 50, 50)
                        lives_explosions_group.add(lives_explosion)
                        lives_explosion_xposition -= 50
                        bullet.kill()



def score_and_lives():
    WINDOW.blit(SCORE, (-70, -90))
    text = font.render(str(score), True, WHITE)
    WINDOW.blit(text, (105, 22))
    WINDOW.blit(LIVE, (360,-90))
    player_live_position_x = WINDOW_WIDTH - 160
    player_live_position_y = 20
    for _ in range(player_lives):
        WINDOW.blit(PLAYER_LIVES_IMAGE,(player_live_position_x, player_live_position_y))
        player_live_position_x += 50
    

def game_over_func():
    score_font = pygame.font.SysFont("verdana", 20)
    score_text = score_font.render(str(score), True, WHITE)
    with open("score.json", "r") as file:
        dic = json.load(file)
        highest_score_string = dic["score"]
    highest_score_font = pygame.font.SysFont("verdana", 20)
    highest_score_text = highest_score_font.render(str(highest_score_string), True, WHITE)
    WINDOW.fill(BLACK)
    WINDOW.blit(GAME_OVER, (WINDOW_WIDTH/2 - 250, -50))
    WINDOW.blit(YOUR_SCORE, (WINDOW_WIDTH/2 - 96, 220))
    WINDOW.blit(HIGHEST_SCORE, (WINDOW_WIDTH/2 - 113, 265))
    WINDOW.blit(score_text, (WINDOW_WIDTH/2 + 84, 322))
    WINDOW.blit(highest_score_text, (WINDOW_WIDTH/2 + 102, 376))
    retry_game_over_button.draw()
    quit_game_over_button.draw()

def draw_game(player):
    WINDOW.fill(BLACK)
    draw_stars()
    global level_timer, text_level_2, game_over
    if player_is_alive == True:
        WINDOW.blit(PLAYER,(player.x, player.y))
    
    else:
        player_explosions_group.draw(WINDOW)
        player_explosions_group.update()
        game_over = True

    if paused_game == False:

        if level_1 == True:
            alien_group.update(70, 100, 3)
            if 0 < level_timer < 260 and times_placed_level_1 == 0:
                WINDOW.blit(text_level_1, (230, 260))

        if level_2 == True:
            alien_group.update(40, 300, 3)
            if -100 < level_timer < 200:
                WINDOW.blit(text_level_2, (230, 260))
         

        if level_3 == True:
            alien_group.update(60, 600, 2)
            if -50 < level_timer < 200:
                WINDOW.blit(text_level_3, (230, 260))

        if level_4 == True:
            if -50 < level_timer < 200:
                WINDOW.blit(text_level_4, (230, 260))
        


        else:
            pass
        bullets_group.update()
        alien_group.draw(WINDOW)
        bullets_group.draw(WINDOW)
    alien_explosions_group.draw(WINDOW)
    alien_explosions_group.update()
    score_and_lives()
    lives_explosions_group.draw(WINDOW)
    lives_explosions_group.update()
    teleport_group.draw(WINDOW)
    teleport_group.update()
    teleport_away_group.draw(WINDOW)
    teleport_away_group.update()
    tech_alien_group.draw(WINDOW)
    tech_alien_group.update()
    braincell_group.draw(WINDOW)
    braincell_group.update()
    pygame.display.update()

def retry():
    global score, player_lives, game_over, player_is_alive, times_placed_level_1, level_1, level_2, level_3, level_4, times_done_level_3
    level_1 = True
    level_2 = False
    level_3 = False
    level_4 = False
    alien_group.empty() 
    bullets_group.empty() 
    tech_alien_group.empty()   
    live_group.empty()  
    alien_explosions_group.empty() 
    player_explosions_group.empty()    
    lives_explosions_group.empty()
    player_is_alive = True
    player_lives = 3
    game_over = False 
    paused_game == False  
    score = 0
    times_placed_level_1 = 0
    times_done_level_3 = 0
    player.x, player.y = WINDOW_WIDTH//2-40, 600
    player_handle()
    

def draw_paused_game():
    resume_pause_button.draw()
    quit_pause_button.draw()

game_over = False
highest_score = {}
times_done_level_4 = 0
times_done_level_3 = 0
#Game loop function
def main():

    global shoot, cooldown, paused_game, countdown, alien_countdown, level_2, live_power, player_lives, level_timer, level_2_text_starter, level_1, level_3, level_3_text_starter, level_1_text_starter, times_placed_level_1, game_over, level_4, level_4_text_starter, times_done_level_4, times_done_level_3
    while True:
        CLOCK.tick(FPS)
        key_pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        #game states checking
        if game_over == False:
            if cooldown > 0:
                cooldown -= 1

            if paused_game == True:
                draw_paused_game()
            else:
                draw_game(player)
                for live in live_group:
                    if player.colliderect(live.rect):
                        if 0 < player_lives < 3:
                            player_lives += 1
                            live.kill()
                
                if shoot:
                    shoot_bullets(-1, player, RED)

                if live_power == True:
                    live_group.update()
                    live_group.draw(WINDOW)

                if level_1 == True and len(alien_group) == 0 and score == 0:
                    level_1_text_starter = True 
                    alien_countdown += 1
                    if alien_countdown == 200:
                        create_aliens(2, 3, 255)
                        level_timer = 300
                        alien_countdown = 0
                        times_placed_level_1 += 1
                        level_1_text_starter = False
                if level_1_text_starter == True:
                    level_timer -=1 
            
                if level_1 == True and len(alien_group) == 0 and score > 0:
                    level_1 = False
                    level_2 = True
                    level_2_text_starter = True
                if level_2_text_starter == True:
                    level_timer -= 1
                if level_2 == True and len(alien_group) == 0:
                    alien_countdown += 1 
                    if alien_countdown == 300:
                        create_aliens(4, 5, 157)
                        level_timer = 200
                        level_2_text_starter = False
                        alien_countdown = 0
                if level_2_text_starter == True:
                    level_timer -= 1

                if level_2 == True and len(alien_group) == 0 and score > 15:
                    alien_countdown = 0
                    level_2 = False
                    level_3 = True
                    level_3_text_starter = True
                if level_3 == True and len(alien_group) == 0 and times_done_level_3 == 0:
                    alien_countdown += 1 
                    if alien_countdown == 400:
                        create_tech_aliens(6, 2, 50)
                        alien_countdown = 0
                        level_timer = 300
                        level_3_text_starter = False
                        times_done_level_3 += 1
                if level_3_text_starter == True:
                    level_timer -= 1
                
                if level_3 == True and len(tech_alien_group) == 0 and times_done_level_3 == 1:
                    alien_countdown = 0
                    level_3 = False
                    level_4 = True
                    level_4_text_starter = True
                if level_4 == True and times_done_level_4 == 0 and times_done_level_3 == 1:
                    alien_countdown += 1 
                    if alien_countdown == 400:
                        create_braincell(350, -150, 2)
                        level_timer = 300
                        level_4_text_starter = False
                        times_done_level_4 += 1
                if level_4_text_starter == True:
                    level_timer -= 1
        
        
        elif game_over == True:
            
            highest_score["score"] = score
            try:

                with open("score.json", "r+") as file:
                    dict = json.load(file)
                if int(dict["score"]) < score:
                    with open("score.json", "w") as file:
                        json.dump(highest_score, file)
                else:
                    pass

            except FileNotFoundError:
                with open("score.json", "w") as file:
                    json.dump(highest_score, file)
            game_over_func()


                
        
        else: 
            pass
            
        player_handle()

        #event handler
        for event in pygame.event.get():   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_game = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and RS_X < mouse_pos[0] < (RS_X + RS_WIDTH) and RS_Y < mouse_pos[1] < (RS_Y + RS_HEIGHT) and paused_game == True:
                paused_game = False
            
            
            if paused_game == True:
                if event.type == pygame.MOUSEBUTTONDOWN and Q_X < mouse_pos[0] < (Q_X + RS_WIDTH) and Q_Y < mouse_pos[1] < (Q_Y + RS_HEIGHT) and paused_game == True:
                    try:
                        os.remove("score.json")
                    except:
                        pass
                    quit()
            if game_over == True: 

                if event.type == pygame.MOUSEBUTTONDOWN and RGO_X < mouse_pos[0] < (RGO_X + RGO_WIDTH) and RGO_Y < mouse_pos[1] < (RGO_Y + RGO_HEIGHT) and player_lives == 0:
                    retry()

                if event.type == pygame.MOUSEBUTTONDOWN and QGO_X < mouse_pos[0] < (QGO_X + QGO_WIDTH) and QGO_Y < mouse_pos[1] < (QGO_Y + QGO_HEIGHT) and player_lives == 0:
                    try:
                        os.remove("score.json")
                    except:
                        pass
                    quit()
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shoot = False
                

            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    os.remove("score.json")
                except:
                    pass
                sys.exit() 
                
        
        pygame.display.update()


def press_to_start_animation(PRESS_TO_START_1,PRESS_TO_START_2, time):  
    global change_time
    press_to_start_animation_list = [PRESS_TO_START_1, PRESS_TO_START_2]
    press_to_start_animation_counter = 0
    press_to_start_actual_image = press_to_start_animation_list[press_to_start_animation_counter]

    if change_time == time:
        WINDOW.blit(press_to_start_actual_image,(0, 0))
        press_to_start_animation_counter += 1
        change_time += 1

        if press_to_start_animation_counter > len(press_to_start_animation_list)-1:
            press_to_start_animation_counter = 0



#Main menu function
def main_menu():
    run = True
    while run:
        CLOCK.tick(FPS_MAIN_MENU)
        time = round(pygame.time.get_ticks()/1000)
        WINDOW.blit(STARTING_SCEEN, (0, 0))
        press_to_start_animation(PRESS_TO_START_1, PRESS_TO_START_2, time)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main() #Game loop call
    pygame.quit()

main_menu()

