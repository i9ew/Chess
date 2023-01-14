from classes.Board import Board
from classes.ButtonW import ButtonW
from classes.ChessGame import ChessGame
from classes.FEN import *
from classes.EvaluationW import EvaluationW
from classes.RectW import RectW
from classes.Scene import Scene
from functions import *


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.bg_color = ColoursRGB.LICHESS
        self.b = Board()
        if get_param_from_client("playFrom"):
            g = ChessGame(get_param_from_client("playFrom"))
        elif get_param_from_client("playFromBE"):
            g = ChessGame(get_param_from_client("playFromBE"))
        else:
            g = ChessGame()
        print("---main_scene---")
        self.b.theme = {"primary_color": ColoursRGB.BROWN,
                        "secondary_color": ColoursRGB.CREAM,
                        "figure_style": "merida",
                        "hud1": [ColoursRGB.GREEN, 150]}
        self.b.corner = [200, 37]
        self.b.board_size = 800
        self.b.game = g
        try:
            self.b.isreversed = not FEN(g.FEN).turn
        except:
            pass

        bg_rect = RectW((*(self.bg_color * 1.8).rgb, 255), [1035, 350 + 80],
                        [530, 400], radius=50)

        self.but2 = ButtonW("Начальная позиция")
        self.but2.text_color = ColoursRGB.LIGHTGREY.rgb
        self.but2.set_font("arial", 40)
        self.but2.set_inactive_bg_colour((*(self.bg_color * 1.8).rgb, 255))
        self.but2.set_hover_bg_colour((*(self.bg_color * 2).rgb, 255))
        self.but2.on_click(self.reset_pos_to_def)
        self.but2.rect = [430, 150]
        self.but2.corner = [1085, 550 + 80]

        self.but3 = ButtonW("Позиция из редактора")
        self.but3.text_color = ColoursRGB.LIGHTGREY.rgb
        self.but3.set_font("arial", 40)
        self.but3.set_inactive_bg_colour((*(self.bg_color * 1.8).rgb, 255))
        self.but3.set_hover_bg_colour((*(self.bg_color * 2).rgb, 255))
        self.but3.on_click(self.reset_pos_to_ed)
        self.but3.rect = [430, 150]
        self.but3.corner = [1085, 400 + 80]

        # print(b)
        ev = EvaluationW([70, 500], [100, 188])
        ev.game = g
        self.elements.append("ev", ev, 0)

        self.elements.append("but2", self.but2, 0)
        self.elements.append("but3", self.but3, 0)
        self.elements.append("bg_rect", bg_rect, -1)
        self.elements.append("main_board", self.b, 0)

    def reset_pos_to_ed(self):
        if get_param_from_client("playFromBE"):
            self.b.game = ChessGame(get_param_from_client("playFromBE"))
            try:
                self.b.isreversed = not FEN(self.b.game.FEN).turn
            except:
                pass

    def reset_pos_to_def(self):
        self.b.game = ChessGame()
        try:
            self.b.isreversed = not FEN(self.b.game.FEN).turn
        except:
            pass

    def input_processing(self, events, events_p):
        super().input_processing(events, events_p)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.goto_scene("menu")

    def update(self):
        super().update()
        if self.b.game.FEN != "nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
            set_param_in_client("playFrom", self.b.game.FEN)
        if self.b.game.is_mate:
            self.scene_manager.goto_scene("screamer")

        if get_param_from_client("playFromBE") and get_param_from_client(
                "playFromBE") != get_param_from_client("playFrom"):
            if self.but3.is_b_hidden():
                self.but3.show()
        else:
            if not self.but3.is_b_hidden():
                self.but3.hide()
