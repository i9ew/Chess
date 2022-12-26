import pygame

from classes.Board import Board
from classes.Scene import Scene
from constants import *
from classes.figures.Rook import Rook
from classes.figures.Knight import Knight

class SecondScene(Scene):
    def __init__(self):
        super().__init__()
        self.b = Board()
        self.b.corner = [150, 100]
        self.b.theme = {"primary_color": ColoursRGB.RED,
                        "secondary_color": ColoursRGB.DARKGREY,
                        "figure_style": "alpha"}
        self.b.board_size = 600
        self.b.place_figure(Rook, "e2", Chess.BLACK_FIGURE)
        self.b.place_figure(Rook, "g4", Chess.WHITE_FIGURE)
        self.b.place_figure(Knight, "f4", Chess.WHITE_FIGURE)

    def input_processing(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    from scenes.main_scene import MainScene
                    self.next_scene = MainScene
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = event.pos

    def update(self):
        self.b.update()

    def render(self, screen):
        self.b.draw(screen)
