from stockfish import Stockfish

from functions import *


class StockfishEngine:
    def __init__(self):
        if __name__ == "__main__":
            path = create_full_path(r"/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")
        else:
            path = create_full_path(
                r"/stockfishEngine/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")

        self.stockfish = Stockfish(path=path, depth=12, parameters={"Threads": 2, "Minimum Thinking Time": 10})
        self.position = ""

    def set_FEN_position(self, fen):
        if self.stockfish.is_fen_valid(fen):
            self.stockfish.set_fen_position(fen)
            self.position = fen
            return True
        else:
            return False

    def is_move_possible(self, from_sqare, to_sqare):
        return self.stockfish.is_move_correct(from_sqare + to_sqare)

    def get_evaluation(self):
        return self.stockfish.get_evaluation()

    def make_move(self, from_sqare, to_sqare):
        if self.position:
            self.stockfish.make_moves_from_current_position([from_sqare + to_sqare])
            self.position = self.stockfish.get_fen_position()

    def all_possible_moves_from(self, from_sqare):
        possibles = []
        for i in range(0, 8):
            for j in range(0, 8):
                coards = indexes_to_coards([i, j])
                if coards != from_sqare and self.is_move_possible(from_sqare, coards):
                    possibles.append(coards)
                if coards != from_sqare and self.is_move_possible(from_sqare, coards + "Q"):
                    possibles.append(coards)
        return possibles

    def best_moves(self, number=1):
        if number > 1:
            return self.stockfish.get_top_moves(number)
        else:
            return self.stockfish.get_best_move()
