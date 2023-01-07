import pygame

from classes.Board import Board
from classes.ChessGame import ChessGame
from classes.Scene import Scene
from constants import *


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        b = Board()
        g = ChessGame()

        print("---main_scene---")
        b.theme = {"primary_color": ColoursRGB.BROWN,
                   "secondary_color": ColoursRGB.CREAM,
                   "figure_style": "merida",
                   "hud1": [ColoursRGB.GREEN, 150]}
        b.corner = [200, 37]
        b.board_size = 600
        b.game = g
        print(b)
        b2 = Board()
        b2.watch_mode = True
        b2.game = g
        b2.board_size = 400
        b2.corner = [900, 100]
        self.elements["main_board"] = b
        self.elements["watch_board"] = b2

    def input_processing(self, events, events_p):
        super().input_processing(events, events_p)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    from scenes.second_scene import SecondScene
                    self.next_scene = SecondScene
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = event.pos
