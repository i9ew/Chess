import os

from stockfish import Stockfish


class StockfishEngine:
    def __init__(self):
        path = os.getcwd() + r"\engine\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
        self.stockfish = Stockfish(path=path, depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})

    def set_FEN_position(self, fen):
        if self.stockfish.is_fen_valid(fen):
            self.stockfish.set_fen_position(fen)
        else:
            raise KeyError("Invalid FEN")

    def is_move_possible(self, from_sqare, to_sqare):
        return self.stockfish.is_move_correct(from_sqare + to_sqare)

    def best_moves(self, number=1):
        if number > 1:
            return self.stockfish.get_top_moves(number)
        else:
            return self.stockfish.get_best_move()
