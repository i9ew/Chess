import os

import pygame

from classes.Board import Board
from classes.ChessGame import ChessGame
from classes.Scene import Scene
from constants import *
from classes.ButtonW import ButtonW

class SecondScene(Scene):
    def __init__(self):
        super().__init__()
        but = ButtonW("Начать игру")
        but.corner = [(RESOLUTION[0] - but.rect[0]) // 2, (RESOLUTION[1] - but.rect[1]) // 2]
        but.text_color = (255, 255, 255, 255)
        but.hover_text_color = (0, 255, 0, 255)
        but.set_inactive_bg_colour((*ColoursRGB.RED.rgb, 50))
        but.on_click(lambda: self.scene_manager.goto_scene("game"))
        self.bg_color = ColoursRGB.LICHESS2.rgb
        self.bg_image_path = os.getcwd() + r"\data\assets\images\logo1.png"
        self.elements["button"] = but

    # def input_processing(self, events, events_p):
    #     super().input_processing(events, events_p)
    #     for event in events:
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_2:
    #                 self.scene_manager.goto_scene("game")
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             mousepos = event.pos
