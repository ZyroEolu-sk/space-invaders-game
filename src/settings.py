import os

# rutas dinámicas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_PATH = os.path.join(BASE_DIR, "assets")

# pantalla
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 650
FPS = 60
FPS_MAIN_MENU = 3

# colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (8, 255, 8)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# configuración del jugador
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60
PLAYER_VEL = 8
STARTING_LIVES = 3

# otros
BULLET_VEL = 8
NUMBER_STARS = 10
STAR_VEL = 6
OVNI_WIDTH, OVNI_HEIGHT = 80, 80
LIVE_VEL = 1