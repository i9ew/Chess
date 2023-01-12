import pyperclip

from classes.Board import Board
from classes.ButtonW import ButtonW
from classes.ChessGame import ChessGame
from classes.EvaluationW import EvaluationW
from classes.Scene import Scene
from functions import *


class BoardEditor(Scene):
    def __init__(self):
        super().__init__()
        print("---b_scene---")
        self.bg_color = ColoursRGB.LICHESS2
        b = Board()
        b.watch_mode = True
        b.corner = [200, 37]
        b.game = ChessGame("8/8/8/8/8/8/8/8 w - - 0 1")

        b2 = Board()
        b2.watch_mode = True
        b2.corner = [1100, 120]
        b2.board_size = 400
        b2.game = ChessGame("8/8/8/8/8/8/8/8 w - - 0 1")
        b2.hide()

        but = ButtonW("Вставить FEN из буфера")
        but.set_hover_bg_colour((*(self.bg_color * 1.8).rgb, 255))
        but.set_rect_bigger_in_x_times(1.07)
        but.text_color = (255, 255, 255, 255)
        but.on_hover(lambda: self.show_buf_board(True))
        but.on_dishover(lambda: self.show_buf_board(False))
        but.corner = [970, 50]

        but2 = ButtonW("Играть из позиции")
        but2.text_color = ColoursRGB.LIGHTGREY.rgb
        but2.set_font("arial", 40)
        but2.set_inactive_bg_colour((*(self.bg_color * 1.8).rgb, 255))
        but2.set_hover_bg_colour((*(self.bg_color * 2).rgb, 255))
        but2.on_click(self.play_from_pos)
        but2.rect = [400, 150]
        but2.corner = [1050, 550]

        r = EvaluationW([100, 700], [50, 50])

        self.elements.append("play_from", but2, 0)
        self.elements.append("main_board", b, 0)
        self.elements.append("buf_board", b2, 0)
        self.elements.append("set_fen", but, 0)
        self.elements.append("evaluation", r, 0)

    def show_buf_board(self, value):
        but = self.elements[0, "set_fen"]
        board = self.elements[0, "buf_board"]
        if value:
            clipboard_content = pyperclip.paste()
            if board.game.is_FEN_correct(clipboard_content):
                but.hover_text_color = (255, 255, 255, 255)
                board.show()
                board.game.set_position(clipboard_content)
                but.on_click(self.past_fen_from_buf_board)
                but.on_click_params([clipboard_content])
                but.set_hover_bg_colour((*(self.bg_color * 1.8).rgb, 255))
            else:
                but.hover_text_color = (255, 0, 0, 255)
                but.set_hover_bg_colour((0, 0, 0, 0))
                but.disconnect_on_click()
        else:
            board.hide()

    def past_fen_from_buf_board(self, fen):
        board = self.elements[0, "main_board"]
        ev = self.elements[0, "evaluation"]
        board.game.set_position(fen)
        ev.game = board.game

    def play_from_pos(self):
        board = self.elements[0, "main_board"]
        if board.game.FEN != "8/8/8/8/8/8/8/8 w - - 0 1":
            set_param_in_client("playFrom", board.game.FEN)
            self.scene_manager.goto_scene("game")
