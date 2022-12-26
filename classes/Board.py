from __future__ import annotations

from classes.FEN import FEN
from functions import *


class Board:
    def __init__(self):
        self.history = []
        self.position = [[" " for __ in range(8)] for __ in range(8)]
        self.theme = {"primary_color": ColoursRGB.BROWN,
                      "secondary_color": ColoursRGB.CREAM,
                      "figure_style": "alpha"}
        self.board_size = 200
        self.sqare_size = self.board_size // 8
        self.corner = [0, 0]
        self.figures = pygame.sprite.Group()

    def draw(self, sc):
        self.draw_board(sc)
        self.figures.draw(sc)

    def update(self):
        self.sqare_size = self.board_size // 8
        for fig in self.figures:
            indexes = coards_to_indexes(fig.placement)
            coards_on_screen = [self.corner[0] + indexes[0] * self.sqare_size,
                                self.corner[1] + indexes[1] * self.sqare_size]
            fig.set_coards(coards_on_screen)
            fig.set_size(self.sqare_size)

    def draw_board(self, sc):
        self.figures.draw(sc)
        for i in range(1, 9):
            for j in range(1, 9):
                color = self.theme["primary_color" if (j + i) % 2 else "secondary_color"]
                pygame.draw.rect(sc, color,
                                 [self.sqare_size * (i - 1) + self.corner[0],
                                  self.sqare_size * (8 - j) + self.corner[1],
                                  self.sqare_size,
                                  self.sqare_size])

    def set_position(self, position, history=None):
        self.position = position
        if history is not None:
            self.history = history

    def set_FEN_position(self, FEN_position):
        position = FEN(FEN_position).position
        for i in position:
            self.place_figure(i[0], i[2], i[1])

    def place_figure(self, figure, coards, color):
        fig = figure(self.figures, self.theme, color, placement=coards)
        indexes = coards_to_indexes(coards)
        self.position[indexes[1]][indexes[0]] = fig.letter

    def __str__(self):
        ans = "\n"
        ans += "-" * 10 + "\n"
        for i in self.position:
            for j in i:
                ans += str(j) + ' '
            ans += "\n"
        ans += "-" * 10 + "\n"
        return ans
