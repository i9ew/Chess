from classes.figures.Rook import Rook
from classes.figures.Knight import Knight
from classes.figures.Bishop import Bishop
from classes.figures.Queen import Queen
from classes.figures.King import King
from classes.figures.Pawn import Pawn
from functions import get_figure, indexes_to_coards
from constants import *

class FEN:
    def __init__(self, fen_str):
        splited = fen_str.split()
        self.position = []
        castled = {"white": {"O-O": "K" in splited[2], "O-O-O": "Q" in splited[2]},
                   "black": {"O-O": "k" in splited[2], "O-O-O": "q" in splited[2]}}
        castled = None
        position_str = splited[0].split("/")

        for i in range(len(position_str)):
            buf = []
            c = 0
            for j in position_str[i]:
                if j.isdigit():
                    c += int(j)
                else:
                    buf.append([*get_figure(j), indexes_to_coards([c, i])])
                    c += 1
            if buf:
                for el in buf:
                    self.position.append(el)

        self.turn = Chess.WHITE_FIGURE if splited[1] == "w" else Chess.BLACK_FIGURE
        self.castled = castled
        self.two_sqare_pawn_move = splited[3]
        self.moves50 = splited[4]
        self.move_number = splited[5]
        self.fen_pos = {
            "position": self.position,
            "turn": splited[1],
            "castled": castled,
            "two_sqare_pawn_move": splited[3],
            "50moves": splited[4],
            "move_number": splited[5]
        }

    def __str__(self):
        print(self.fen_pos)
        return ""
