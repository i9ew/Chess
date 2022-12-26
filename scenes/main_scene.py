import pygame

from classes.Board import Board
from classes.Scene import Scene
from constants import *
from classes.figures.Rook import Rook


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.b = Board()
        self.b2 = Board()
        self.b2.corner = [400, 400]
        self.b2.theme = {"primary_color": ColoursRGB.BLUE,
                         "secondary_color": ColoursRGB.CREAM,
                         "figure_style": "alpha"}
        self.b2.place_figure(Rook, "a1", Chess.WHITE_FIGURE)
        print(self.b2)

    def input_processing(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    from scenes.second_scene import SecondScene
                    self.next_scene = SecondScene
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = event.pos

    def update(self):
        self.b.update()
        self.b2.update()

    def render(self, screen):
        self.b.draw(screen)
        self.b2.draw(screen)
