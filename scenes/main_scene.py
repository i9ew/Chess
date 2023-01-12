import pygame

from classes.Board import Board
from classes.ChessGame import ChessGame
from classes.Scene import Scene
from constants import *
from classes.ButtonW import ButtonW
from classes.EvaluationW import EvaluationW
from constants import *
from functions import *


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.bg_color = ColoursRGB.LICHESS
        b = Board()
        if get_param_from_client("playFrom"):
            g = ChessGame(get_param_from_client("playFrom"))
        else:
            g = ChessGame()
        print("---main_scene---")
        b.theme = {"primary_color": ColoursRGB.BROWN,
                   "secondary_color": ColoursRGB.CREAM,
                   "figure_style": "merida",
                   "hud1": [ColoursRGB.GREEN, 150]}
        b.corner = [200, 37]
        b.board_size = 800
        b.game = g
        # print(b)
        # ev = EvaluationW([70, 500], [100, 37])
        # ev.game = g
        # self.elements.append("ev", ev, 0)
        self.elements.append("main_board", b, 0)

    # def input_processing(self, events, events_p):
    #     super().input_processing(events, events_p)
    #     for event in events:
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_2:
    #                 self.scene_manager.goto_scene("menu")
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             mousepos = event.pos
