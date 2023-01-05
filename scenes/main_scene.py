import pygame

from classes.Board import Board
from classes.Scene import Scene
from constants import *

class MainScene(Scene):
    def __init__(self):
        super().__init__()
        b = Board()


        b.theme = {"primary_color": ColoursRGB.BROWN,
                      "secondary_color": ColoursRGB.CREAM,
                      "figure_style": "merida"}

        b.set_FEN_position("rnb1kb1r/1nqppppp/p1p1q3/2N5/1B3P2/N1P5/PP1PP1PP/R1BQ1RK1 w Qkq - 0 1")
        print("---main_scene---")
        print(b)
        b.corner = [200, 37]
        b.board_size = 600
        self.elements["main_board"] = b

    def input_processing(self, events):
        super().input_processing(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    from scenes.second_scene import SecondScene
                    self.next_scene = SecondScene
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = event.pos

