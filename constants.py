import pygame
import os

class Colour:
    def __init__(self, r, g, b):
        self.rgb = [r, g, b]

    def __mul__(self, other):
        rgb = [int(self.rgb[0] * other), int(self.rgb[1] * other), int(self.rgb[2] * other)]
        rgb[0] = max(min(rgb[0], 255), 0)
        rgb[1] = max(min(rgb[1], 255), 0)
        rgb[2] = max(min(rgb[2], 255), 0)
        return Colour(*rgb)


# Colours
class ColoursRGB:
    BLACK = Colour(0, 0, 0)
    WHITE = Colour(255, 255, 255)
    RED = Colour(255, 0, 0)
    GREEN = Colour(0, 255, 0)
    LIGHTGREEN = Colour(204, 255, 204)
    BLUE = Colour(0, 0, 255)
    BROWN = Colour(152, 118, 84)
    CREAM = Colour(253, 244, 227)
    DARKGREY = Colour(64, 64, 64)
    LIGHTGREY = Colour(187, 187, 187)
    LICHESS = Colour(38, 36, 33)
    LICHESS2 = Colour(22, 21, 18)


class Chess:
    WHITE_FIGURE = True
    BLACK_FIGURE = False
    NORMAL_MOVE = 1
    INCORRECT_MOVE = 0
    PAWN_TRANSFORMATION_WHITE = 3
    PAWN_TRANSFORMATION_BLACK = 2
    CHECK = 4
    MATE = 5
    STALEMATE = 6


TIMER_EVENT_20TPS = pygame.USEREVENT + 1
TIMER_EVENT_10TPS = pygame.USEREVENT + 2

user_path = os.path.join(os.getcwd(), "data", "username.txt")
base_path = os.path.join(os.getcwd(), "data", "sqlbase")


# Screen
RESOLUTION = 1600, 900
FPS = 60
NAME = "chess"
BG = ColoursRGB.DARKGREY
