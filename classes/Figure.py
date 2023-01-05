import os

import pygame

from constants import *
from functions import load_image, coards_to_indexes


class Figure(pygame.sprite.Sprite):
    def __init__(self, group, theme, color, placement=""):
        super().__init__(group)
        self.color = color
        self.style = theme["figure_style"]
        self.letter = self.get_figure_letter()
        self.image_path = self.get_figure_path()
        self.image = load_image(self.image_path)
        self.rect = self.image.get_rect()
        self.placement = placement
        self.coards = [50, 50]
        self.rect.x = self.coards[0]
        self.rect.y = self.coards[1]

    def refresh_theme(self):
        self.image_path = self.get_figure_path()
        self.image = load_image(self.image_path)

    def get_figure_path(self):
        return os.getcwd() + rf"\classes\figures\figure_styles\{self.style}\{self.color}{self.letter}.png"

    def set_coards(self, coards):
        self.coards = coards
        self.rect.x = self.coards[0]
        self.rect.y = self.coards[1]

    def calculate_coards(self, corner, sqare_size, isreversed):
        indexes = coards_to_indexes(self.placement)
        coards_on_screen = [indexes[0] * sqare_size,
                            indexes[1] * sqare_size]
        if isreversed:
            coards_on_screen = [7 * sqare_size - coards_on_screen[0], 7 * sqare_size - coards_on_screen[1]]

        coards_on_screen = [coards_on_screen[0] + corner[0], coards_on_screen[1] + corner[1]]

        self.set_coards(coards_on_screen)
        self.set_size(sqare_size)


    def set_size(self, size):
        im = load_image(self.image_path)
        self.image = pygame.transform.scale(im, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = self.coards[0]
        self.rect.y = self.coards[1]

    def get_figure_letter(self):
        sl = {
            "King": "K",
            "Rook": "R",
            "Knight": "N",
            "Pawn": "P",
            "Bishop": "B",
            "Queen": "Q"

        }
        try:
            if self.color == Chess.WHITE_FIGURE:
                return sl[self.__class__.__name__]
            else:
                return sl[self.__class__.__name__].lower()
        except KeyError:
            raise KeyError(f"There is no such figure in chess '{self.__class__.__name__}'")

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.__class__.__name__
