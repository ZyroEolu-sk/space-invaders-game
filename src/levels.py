"""Definición de los niveles del juego.

Cada nivel es una entrada de LEVELS, y el resto del juego los recorre por
índice sin saber cuántos hay. Añadir un nivel nuevo es añadir un diccionario a
esta lista: no hay que tocar reset_game(), ni el bucle principal, ni los
carteles, ni el fondo de estrellas.

Claves de cada nivel:

  label                  Texto del cartel al empezar la oleada.
  star_dir               Dirección del scroll de estrellas del fondo.
  alien_move             Parámetros de Aliens.update(), es decir
                         (distancia, probabilidad, velocidad). None si el
                         nivel no usa aliens básicos.
  spawn_delay            Frames de espera antes de soltar la oleada.
  text_timer             Frames que dura el cartel del nivel.
  spawn                  Función que suelta la oleada; recibe el Game.
  keep_spawning          Mientras devuelva True se siguen soltando oleadas.
                         Cuando devuelva False y los grupos estén limpios, se
                         pasa al siguiente nivel.
  clear_groups           Grupos que deben estar vacíos para soltar la
                         siguiente oleada o para avanzar de nivel.
  label_first_wave_only  Si está, el cartel solo sale antes de la primera
                         oleada del nivel.
"""

import random

from settings import STAR_VEL
from entities import Braincell, TechAlien


def _spawn_tech_aliens(game):
    for _ in range(6):
        game.tech_alien_group.add(
            TechAlien(random.randint(0, 800), random.randint(-50, 100), 2, 50)
        )


LEVELS = [
    {
        "label": "LEVEL 1",
        "star_dir": (0, STAR_VEL),
        "alien_move": (70, 100, 3),
        "spawn_delay": 200,
        "text_timer": 300,
        "spawn": lambda game: game.create_aliens(2, 3, 255),
        # Se repiten oleadas hasta que el jugador mate a su primer alien.
        "keep_spawning": lambda game: game.score == 0,
        "clear_groups": ("alien_group",),
        "label_first_wave_only": True,
    },
    {
        "label": "LEVEL 2",
        "star_dir": (STAR_VEL, STAR_VEL // 2),
        "alien_move": (40, 300, 3),
        "spawn_delay": 300,
        "text_timer": 200,
        "spawn": lambda game: game.create_aliens(4, 5, 157),
        "keep_spawning": lambda game: game.score <= 15,
        "clear_groups": ("alien_group",),
    },
    {
        "label": "LEVEL 3",
        "star_dir": (-STAR_VEL, STAR_VEL // 2),
        "alien_move": (60, 600, 2),
        "spawn_delay": 400,
        "text_timer": 300,
        "spawn": _spawn_tech_aliens,
        # Una sola oleada: cuando caigan todos, se pasa al jefe.
        "keep_spawning": lambda game: game.waves_spawned == 0,
        "clear_groups": ("alien_group", "tech_alien_group"),
    },
    {
        "label": "LEVEL 4",
        "star_dir": (0, -STAR_VEL),
        # El jefe invoca aliens básicos, pero este nivel no los mueve.
        "alien_move": None,
        "spawn_delay": 400,
        "text_timer": 300,
        "spawn": lambda game: game.braincell_group.add(Braincell(350, -150, 2)),
        "keep_spawning": lambda game: game.waves_spawned == 0,
        "clear_groups": ("braincell_group",),
    },
]

# Dirección del fondo cuando ya no queda nivel, es decir con la partida ganada.
STAR_DIR_DEFAULT = (0, -STAR_VEL)
