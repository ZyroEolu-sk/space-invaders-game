"""Carga de imágenes con caché.

Antes cada enemigo leía sus imágenes del disco en su propio `__init__`: un
TechAlien abría 10 PNG al nacer y un Braincell, 66 escalados a 400x400. Y como
el jefe invoca TechAliens en mitad del combate, eso eran lecturas de disco en
plena partida. En el navegador, con el sistema de ficheros virtual, se nota más
todavía.

Aquí cada imagen se carga una sola vez y se reparte la misma Surface. Se pueden
compartir porque el juego solo las dibuja: nunca pinta encima de ellas. Si
algún día hace falta modificar una, hay que sacarle una copia con `.copy()`
antes, o el cambio se vería en todos los sprites que la compartan.
"""

import os
from functools import lru_cache

import pygame


@lru_cache(maxsize=None)
def image(path, size=None):
    """Devuelve la imagen, escalada si se indica tamaño. Cacheada."""
    img = pygame.image.load(path)
    if size is not None:
        img = pygame.transform.scale(img, size)
    return img


def frames(folder, pattern, indices, size):
    """Fotogramas de una animación, ya cacheados.

    `pattern` lleva un hueco para el número, por ejemplo "pixil-frame-{}.png".
    `indices` es cualquier secuencia, así que sirve para animaciones al revés.
    """
    return [image(os.path.join(folder, pattern.format(i)), size) for i in indices]
