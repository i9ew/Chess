import os

import pygame


def classname(clas):
    return clas.__class__.__name__


def load_image(path, colorkey=None):
    # fullname = os.path.join('data', name)
    fullname = path
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def coards_to_indexes(coards):
    sl = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }
    return [sl[coards[0]], 8 - int(coards[1])]
