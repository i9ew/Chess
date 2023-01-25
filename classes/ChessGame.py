import chess

from classes.FEN import FEN
from classes.StockfishM import StockfishEngine
from constants import *
from constants import Chess as ChessC
from classes.VoiceControl import VoiceControl


class ChessGame:
    def __init__(self, FEN_position="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.FEN_position = FEN_position
        self.engine = None
        self.play_on_boards = []
        self.engine = StockfishEngine()
        self.engine.set_FEN_position(self.FEN_position)
        self.board = chess.Board(self.FEN_position)
        self.pos_history = []
        self.moves_history = []
        self.evaluation = self.get_evaluation() if FEN_position else None

        self.voice_control_enable = True

    def move_request(self, from_sqare, to_square):
        fig = self.play_on_boards[0].get_from_sqare(from_sqare)
        if self.engine.is_move_possible(from_sqare, to_square + "Q"):
            if fig.letter == "p" and to_square[1] == "1" and len(to_square) == 2:
                return Chess.PAWN_TRANSFORMATION_BLACK
            if fig.letter == "P" and to_square[1] == "8" and len(to_square) == 2:
                return Chess.PAWN_TRANSFORMATION_WHITE
        if self.engine.is_move_possible(from_sqare, to_square):
            self.make_move(from_sqare, to_square)
            self.evaluation = self.get_evaluation()
            if self.is_mate:
                return Chess.MATE
            if self.is_check:
                return Chess.CHECK
            if self.is_stalemate:
                return Chess.STALEMATE
            return Chess.NORMAL_MOVE
        return Chess.INCORRECT_MOVE

    def is_FEN_correct(self, fen_pos):
        return self.engine.stockfish.is_fen_valid(fen_pos)

    def set_position(self, fen_pos):
        self.engine.set_FEN_position(fen_pos)
        self.board.set_board_fen(fen_pos.split()[0])
        self.evaluation = self.get_evaluation()
        self.FEN_position = self.engine.position
        for board in self.play_on_boards:
            board.unselect_all()
            board.set_FEN_position(fen_pos)
            try:
                board.isreversed = True if self.turn == ChessC.BLACK_FIGURE else False
            except:
                pass

    def make_move(self, from_sqare, to_square):
        move = ""
        fig = self.play_on_boards[0].get_from_sqare(from_sqare)
        move_l = fig.letter.upper() if fig.letter.upper() != "P" else ""
        move += f"{move_l}{from_sqare}-{to_square}"
        self.pos_history.append(self.engine.position)
        self.engine.make_move(from_sqare, to_square)
        self.board.set_board_fen(self.engine.position.split()[0])
        self.board.turn = self.turn
        for board in self.play_on_boards:
            board.set_FEN_position(self.engine.position)
            try:
                board.isreversed = True if self.turn == ChessC.BLACK_FIGURE else False
            except:
                pass
        print(self.play_on_boards[0])
        if self.is_mate:
            move += "#"
        elif self.is_check:
            move += "+"
        self.moves_history.append([self.move_number, self.turn, move])

    def pop_history(self):
        if self.pos_history:
            poped = self.pos_history.pop()
            self.moves_history.pop()
            self.set_position(poped)
            return poped

    def get_evaluation(self):
        return self.engine.get_evaluation()

    @property
    def FEN(self):
        return self.engine.position

    @property
    def last_move(self):
        if self.moves_history:
            return self.moves_history[-1]

    @property
    def turn(self):
        return FEN(self.engine.position).turn

    @property
    def move_number(self):
        return FEN(self.engine.position).move_number

    @property
    def is_check(self):
        return self.board.is_check()

    @property
    def is_mate(self):
        return self.board.is_checkmate()

    @property
    def is_stalemate(self):
        return self.board.is_stalemate()

    def all_possible_moves_from(self, sqare):
        return self.engine.all_possible_moves_from(sqare)

    def update(self):
        if self.voice_control_enable and VoiceControl.is_move_request():
            move = VoiceControl.get_move_from_word_contol()
            try:
                if len(move) == 4:
                    self.move_request(move[:2], move[2:])
                elif move == "O-O":
                    print(self.board.king(self.turn))
            except:
                pass
            VoiceControl.clear_voice_control()
