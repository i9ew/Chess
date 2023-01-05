from __future__ import annotations

from classes.FEN import FEN
from functions import *


class Board:
    def __init__(self):
        self.history = []
        self.position = [[" " for __ in range(8)] for __ in range(8)]
        self._theme = {"primary_color": ColoursRGB.BROWN,
                      "secondary_color": ColoursRGB.CREAM,
                      "figure_style": "alpha"}
        self._board_size = 720
        self.sqare_size = self.board_size // 8
        self._corner = [0, 0]
        self.figures = pygame.sprite.Group()

        self.font_size = self.board_size // 28
        self.fontnum_size = self.board_size // 30
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.fontnum = pygame.font.SysFont("arial", self.fontnum_size)
        self.isreversed = False

    def draw(self, sc):
        self.draw_board(sc, Chess.BLACK_FIGURE if self.isreversed else Chess.WHITE_FIGURE)
        self.figures.draw(sc)

    def input_processing(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.isreversed = not self.isreversed
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = event.pos

    def draw_board(self, sc, turn):
        for i in range(1, 9):
            for j in range(1, 9):
                color = self.theme["primary_color" if ((j + i + 1) % 2) else "secondary_color"]
                pygame.draw.rect(sc, color,
                                 [self.sqare_size * (i - 1) + self.corner[0],
                                  self.sqare_size * (8 - j) + self.corner[1],
                                  self.sqare_size,
                                  self.sqare_size])
        rendered = [[], []]
        for i in range(1, 9):
            col = self.theme["secondary_color" if i % 2 else "primary_color"]
            if turn == Chess.WHITE_FIGURE:
                rendered[0].append(self.font.render(chr(ord("a") - 1 + i), True, col))
                rendered[1].append(self.fontnum.render(str(9 - i), True, col))
            else:
                rendered[0].append(self.font.render(chr(ord("h") + 1 - i), True, col))
                rendered[1].append(self.fontnum.render(str(i), True, col))
        for i in range(1, 9):
            sc.blit(rendered[0][i - 1],
                    (self.sqare_size * (i - 1) + self.corner[0],
                     self.sqare_size * 8 + self.corner[1] - self.font_size - 3 * self.board_size // 720))
            sc.blit(rendered[1][i - 1],
                    (self.sqare_size * 8 + self.corner[0] - self.fontnum_size + 10 * self.board_size // 720, self.sqare_size * (i - 1) + self.corner[1]))

    @property
    def isreversed(self):
        return self._isreversed

    @isreversed.setter
    def isreversed(self, val):
        self._isreversed = val
        for fig in self.figures:
            fig.calculate_coards(self.corner, self.sqare_size, self.isreversed)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        self._theme = value
        for fig in self.figures:
            fig.style = self._theme["figure_style"]
            fig.refresh_theme()

    @property
    def board_size(self):
        return self._board_size

    @board_size.setter
    def board_size(self, value):
        self._board_size = value
        self.sqare_size = self.board_size // 8
        self.font_size = self.board_size // 28
        self.fontnum_size = self.board_size // 30
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.fontnum = pygame.font.SysFont("arial", self.fontnum_size)
        for fig in self.figures:
            indexes = coards_to_indexes(fig.placement)
            coards_on_screen = [self.corner[0] + indexes[0] * self.sqare_size,
                                self.corner[1] + indexes[1] * self.sqare_size]
            fig.set_coards(coards_on_screen)
            fig.set_size(self.sqare_size)

    @property
    def corner(self):
        return self._corner

    @corner.setter
    def corner(self, value):
        self._corner = value
        for fig in self.figures:
            indexes = coards_to_indexes(fig.placement)
            coards_on_screen = [self.corner[0] + indexes[0] * self.sqare_size,
                                self.corner[1] + indexes[1] * self.sqare_size]
            fig.set_coards(coards_on_screen)

    def set_position(self, position, history=None):
        self.position = position
        if history is not None:
            self.history = history

    def set_FEN_position(self, FEN_position):
        position = FEN(FEN_position).position
        for i in position:
            self.place_figure(i[0], i[2], i[1])

    def clear_board(self):
        self

    def place_figure(self, figure, coards, color):
        fig = figure(self.figures, self.theme, color, placement=coards)
        indexes = coards_to_indexes(coards)
        self.position[indexes[1]][indexes[0]] = fig.letter
        # indexes = coards_to_indexes(fig.placement)
        # coards_on_screen = [self.corner[0] + indexes[0] * self.sqare_size,
        #                     self.corner[1] + indexes[1] * self.sqare_size]
        # fig.set_coards(coards_on_screen)
        # fig.set_size(self.sqare_size)
        fig.calculate_coards(self.corner, self.sqare_size, False)

    def __str__(self):
        ans = "\n"
        ans += "-" * 10 + "\n"
        for i in self.position:
            for j in i:
                ans += str(j) + ' '
            ans += "\n"

        ans += "White: "
        buf = []
        for i in self.figures:
            if i.color == Chess.WHITE_FIGURE:
                buf.append(str(i).upper() + i.placement)
        ans += ", ".join(sorted(buf, key=lambda x: (["K", "Q", "R", "B", "N", "P"].index(x[0]), x[1:]))).replace("P", "")
        ans += "\nBlack: "
        buf = []
        for i in self.figures:
            if i.color == Chess.BLACK_FIGURE:
                buf.append(str(i).upper() + i.placement)
        ans += ", ".join(sorted(buf, key=lambda x: (["K", "Q", "R", "B", "N", "P"].index(x[0]), x[1:]))).replace("P", "")
        ans += "\n" + "-" * 10 + "\n"
        return ans
