import pygame

from constants import *


class Board:
    def __init__(self):
        self.history = []
        self.position = []
        self.theme = {"primary_color": ColoursRGB.BROWN,
                      "secondary_color": ColoursRGB.CREAM}
        self.board_size = 200
        self.sqare_size = self.board_size // 8
        self.corner = [0, 0]

    def draw(self, sc):
        self.sqare_size = self.board_size // 8
        for i in range(1, 9):
            for j in range(1, 9):
                color = self.theme["primary_color" if (j + i) % 2 else "secondary_color"]
                pygame.draw.rect(sc, color,
                                 [self.sqare_size * i + self.corner[0], self.sqare_size * (9 - j) + self.corner[1],
                                  self.sqare_size,
                                  self.sqare_size])

    def set_position(self, position, history=None):
        self.position = position
        if history is not None:
            self.history = history

    def __str__(self):
        ans = ""
        for i in self.position:
            for j in i:
                ans += str(j) + ' '
            ans += "\n"
        return ans
