import pygame

from classes.Board import Board
from classes.Scene import Scene
from constants import *



class SecondScene(Scene):
    def __init__(self):
        super().__init__()
        self.b = Board()
        self.b.corner = [250, 400]
        self.b.theme = {"primary_color": ColoursRGB.RED,
                        "secondary_color": ColoursRGB.DARKGREY}
        self.b.board_size = 400

    def input_processing(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    from scenes.main_scene import MainScene
                    self.next_scene = MainScene
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = event.pos

    def render(self, screen):
        self.b.draw(screen)
