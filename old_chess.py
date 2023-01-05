import os

import pygame


def classname(clas):
    return clas.__class__.__name__


class ColoursRGB:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (204, 255, 204)
    BLUE = (0, 0, 255)
    BROWN = (152, 118, 84)
    CREAM = (253, 244, 227)
    GREY = (64, 64, 64)
    GREY2 = (187, 187, 187)


class Colour:
    WHITE = 1
    BLACK = 0

    def __init__(self):
        self.turn = self.WHITE

    @staticmethod
    def colour_change(colour):
        return int(not colour)

    def turn_change(self):
        return int(not self.turn)


class Empty:
    def __init__(self):
        self.attacked_white = False
        self.attacked_black = False
        self.draw_circles = False

    def __str__(self):
        return "*"

    def __repr__(self):
        return "*"


class Board:
    empty_board = [[Empty() for i in range(8)] for j in range(8)]

    def __init__(self, board=empty_board):
        self.board = board
        self.wk_checked = False
        self.bk_checked = False
        self.wk_mated = False
        self.bk_mated = False
        self.history = [[board, 0]]

    def __str__(self):
        ans = ""
        for i in self.board:
            for j in i:
                ans += str(j) + ' '
            ans += "\n"
        return ans

    def __call__(self, coards):
        indexes = Board.pos_to_indexes(coards)
        return self.board[indexes[0]][indexes[1]]

    @staticmethod
    def coards_to_pos(c):
        ltn = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8
        }
        try:
            return [ltn[c[0]], int(c[1])]
        except:
            return ["Error", "Error"]

    @staticmethod
    def pos_to_coards(pos):
        # numbers to chess coards
        ltn = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h"
        }
        try:
            return f"{ltn[pos[0]]}{pos[1]}"
        except:
            return ["Error", "Error"]

    @staticmethod
    def correct_coards(row, col):
        return 1 <= row <= 8 and 1 <= col <= 8

    @staticmethod
    def colour_of_square(sq):
        sq = Board.coards_to_pos(sq)
        if not Board.correct_coards(sq[0], sq[1]):
            return "Error"
        elif sq[0] % 2 == sq[1] % 2:
            return Colour.BLACK
        return Colour.WHITE

    @staticmethod
    def make_move(mfrom, mto, boardch):
        buf = boardch(Board.coards_to_pos(mfrom))
        buf.coards = mto
        mfrom, mto = Board.coards_to_pos(mfrom), Board.coards_to_pos(mto)
        bufb = boardch
        mfrom, mto = Board.pos_to_indexes(mfrom), Board.pos_to_indexes(mto)
        bufb.board[mfrom[0]][mfrom[1]] = Empty()
        bufb.board[mto[0]][mto[1]] = buf
        return bufb

    @staticmethod
    def king_checked(boardch, colo):
        king_coards = "No king on the board"
        for i in range(8):
            for j in range(8):
                if classname(boardch[i][j]) == "King" and boardch[i][j].color == colo:
                    king_coards = Board.pos_to_indexes(boardch[i][j].get_pos())
        # rook and queen

    @staticmethod
    def colour_of_pos(sq):
        if not Board.correct_coards(sq[0], sq[1]):
            return "Error"
        elif sq[0] % 2 == sq[1] % 2:
            return Colour.BLACK
        return Colour.WHITE

    @staticmethod
    def pos_to_indexes(coards):
        return [8 - coards[1], coards[0] - 1]

    def place_figure(self, figure):
        indexes = self.pos_to_indexes(figure.get_pos())
        self.board[indexes[0]][indexes[1]] = figure

    def place_figures(self, listf):
        for i in listf:
            self.place_figure(i)

    @staticmethod
    def get_figure_letter(fig):
        sl = {
            "King": "K",
            "Rook": "R",
            "Knight": "N",
            "Pawn": "P",
            "Bishop": "B",
            "Queen": "Q"

        }
        return sl[fig]

    @staticmethod
    def get_figure_path(fig, style, color):
        return os.getcwd() + rf"\data\figures\{style}\{'b' if color == Colour.BLACK else 'w'}{Board.get_figure_letter(fig)}.png"

    def __getitem__(self, item):
        return self.board[item]

    @staticmethod
    def disselect_all(boardc):
        for i in range(8):
            for j in range(8):
                if classname(boardc[i][j]) != "Empty":
                    boardc[i][j].selected = False

    @staticmethod
    def convert_coards_to_color(coa, colo):
        if colo == Colour.BLACK:
            return 9 - coa[0], 9 - coa[1]
        return coa


class Figure:
    def __init__(self, coards, color, style):
        self.coards = coards
        self.color = color
        self.path = Board.get_figure_path(self.__class__.__name__, style, color)
        self.selected = False

    def open_image(self):
        print(self.path)
        os.startfile(self.path)

    def get_pos(self):
        return Board.coards_to_pos(self.coards)

    def __str__(self):
        return Board.get_figure_letter(self.__class__.__name__)

    def __repr__(self):
        return Board.get_figure_letter(self.__class__.__name__)


class King(Figure):
    def can_move(self, new_coards, boardch):
        new_coards = Board.coards_to_pos(new_coards)
        try:
            if abs(self.get_pos()[0] - new_coards[0]) in [0, 1] and \
                    abs(self.get_pos()[1] - new_coards[1]) in [0, 1] \
                    and self.get_pos() != new_coards \
                    and Board.correct_coards(new_coards[0], new_coards[1]):
                return True
        except:
            pass
        return False


class Rook(Figure):
    def can_move(self, new_coards, boardch):
        new_coards = Board.coards_to_pos(new_coards)
        try:
            if Board.correct_coards(new_coards[0], new_coards[1]) and (self.get_pos()[0] == new_coards[0] or \
                                                                       self.get_pos()[1] == new_coards[
                                                                           1]) and self.get_pos() != new_coards:
                if self.get_pos()[0] == new_coards[0]:
                    for i in range(abs(self.get_pos()[1] - new_coards[1]) - 1):
                        if classname(
                                boardch([self.get_pos()[0], min(self.get_pos()[1], new_coards[1]) + i + 1])) != "Empty":
                            return False
                if self.get_pos()[1] == new_coards[1]:
                    for i in range(abs(self.get_pos()[0] - new_coards[0]) - 1):
                        if classname(
                                boardch([min(self.get_pos()[0], new_coards[0]) + i + 1, self.get_pos()[1]])) != "Empty":
                            return False
                if classname(boardch(new_coards)) != "Empty" and boardch(new_coards).color == self.color:
                    return False
                return True
        except:
            pass
        return False


class Game:
    def __init__(self, name, size, FPS):
        pygame.init()
        pygame.mixer.init()
        self.name = name
        self.size = size
        self.FPS = FPS
        self.sqare_size = 90
        self.font_size = 25
        self.fontnum_size = 22
        self.spaces = 0
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.fontnum = pygame.font.SysFont("arial", self.fontnum_size)
        self.board_player_color = Colour.WHITE
        self.board_draw_color = Colour.WHITE
        self.show_text = True

    def draw_matrix(self, screen, board2):
        for i in board2.board:
            for j in i:
                # k = King("h4", Colour.WHITE, "alpha", "board_here")
                if classname(j) != "Empty":
                    self.draw_image(screen, j.path, self.rowcol_to_coards(j.get_pos(), self.board_draw_color))

    def find_selected(self, boardc):
        for i in boardc.board:
            for j in i:
                if classname(j) != "Empty" and j.selected:
                    return j
        return None

    def draw_selected_possible_moves(self, sc, boardc, colo):
        for i in boardc.board:
            for j in i:
                if classname(j) != "Empty" and j.selected:
                    for h in range(1, 9):
                        for hh in range(1, 9):
                            if j.can_move(Board.pos_to_coards([h, hh]), boardc):
                                self.draw_circle(sc, Board.convert_coards_to_color([h, hh], colo))
                    break

    def run(self):
        board = Board()
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.name)
        clock = pygame.time.Clock()
        running = True
        # wk = King("b8", Colour.WHITE, "alpha")
        # bk = King("a6", Colour.BLACK, "alpha")
        # wr2 = Rook("d3", Colour.WHITE, "alpha")
        # wr = Rook("c3", Colour.WHITE, "alpha")
        # br = Rook("d7", Colour.BLACK, "alpha")
        # board.place_figures([wk, bk, wr, wr2, br])
        # Board.king_checked(board, Colour.WHITE)
        print(board)
        while running:
            screen.fill(ColoursRGB.GREY)
            self.draw_empy_board(screen, self.board_draw_color, self.show_text)
            self.draw_turn_sqare(screen, self.board_player_color)
            self.draw_matrix(screen, board)
            self.draw_selected_possible_moves(screen, board, self.board_draw_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.board_draw_color = Colour.colour_change(self.board_draw_color)
                        Board.disselect_all(board)
                    if event.key == pygame.K_t:
                        self.show_text = not self.show_text
                    if event.key == pygame.K_e:
                        pass
                        # self.board_player_color = Colour.colour_change(self.board_player_color)
                        # self.board_draw_color = self.board_player_color
                        # Board.disselect_all(board)
                        # Ломает  логику игры, лучше не раскоменчивать
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = event.pos
                    if self.calculate_sqare(mousepos) != "Error":
                        mousepos = Board.convert_coards_to_color(Board.coards_to_pos(self.calculate_sqare(event.pos)),
                                                                 self.board_draw_color)
                        mousepos = Board.pos_to_coards(mousepos)
                        if event.button == 1:
                            sqare = Board.pos_to_indexes(Board.coards_to_pos(mousepos))
                            if self.find_selected(board) is not None and self.find_selected(board).can_move(mousepos,
                                                                                                            board):
                                move = f"{str(self.find_selected(board))}{self.find_selected(board).coards}-{str(self.find_selected(board))}{mousepos}"
                                board = Board.make_move(self.find_selected(board).coards, mousepos, board)
                                Board.disselect_all(board)
                                board.history.append([board.board, move])
                                print(board.history[-1][1])
                                self.board_player_color = Colour.colour_change(self.board_player_color)
                                self.board_draw_color = self.board_player_color
                            else:
                                if classname(board[sqare[0]][sqare[1]]) != "Empty" and board[sqare[0]][sqare[1]].color == self.board_player_color:
                                    v = not board[sqare[0]][sqare[1]].selected
                                    Board.disselect_all(board)
                                    board[sqare[0]][sqare[1]].selected = v
                                    # print(("White" if board[sqare[0]][sqare[1]].color == Colour.WHITE else "Black"),
                                    #       classname(board[sqare[0]][sqare[1]]).lower(),
                                    #       "selected" if board[sqare[0]][sqare[1]].selected else "disselected")
                                else:
                                    Board.disselect_all(board)
                        elif event.button == 3:
                            pass

            pygame.display.update()
            clock.tick(self.FPS)
        # for i in range(1, len(board.history)):
        #     print(board.history[i][1])

    def calculate_sqare(self, pos):
        if self.sqare_size < pos[0] < self.sqare_size * 9 and self.sqare_size < pos[1] < self.sqare_size * 9:
            c1, c2 = (pos[0] - 1) // 90, 9 - (pos[1] - 1) // 90
            return Board.pos_to_coards((c1, c2))
        else:
            return "Error"

    def draw_turn_sqare(self, sc, turn):
        turn_color = ColoursRGB.WHITE if turn == Colour.WHITE else ColoursRGB.BLACK
        pygame.draw.rect(sc, ColoursRGB.GREEN, [0, 0, self.sqare_size, self.sqare_size])
        pygame.draw.rect(sc, turn_color,
                         [self.sqare_size // 8, self.sqare_size // 8, self.sqare_size / 8 * 6, self.sqare_size / 8 * 6])

    def rowcol_to_coards(self, pos, turn):
        if turn == Colour.BLACK:
            pos[0], pos[1] = 9 - pos[0], 9 - pos[1]
        coards = [(self.sqare_size + self.spaces) * pos[0] + 5, (self.sqare_size + self.spaces) * (10 - pos[1]) - 5]
        return coards

    @staticmethod
    def draw_image(sc, path, pos):
        im = pygame.image.load(path)
        rect = im.get_rect(
            bottomleft=(pos[0], pos[1]))
        sc.blit(im, rect)

    def draw_circle(self, sc, coards):
        pygame.draw.circle(sc, ColoursRGB.GREY2, [(self.sqare_size + self.spaces) * coards[0] + self.sqare_size // 2,
                                                  (self.sqare_size + self.spaces) * (
                                                          9 - coards[1]) + self.sqare_size // 2,
                                                  ], self.sqare_size // 5)

    def draw_empy_board(self, sc, bturn, show_text):
        for i in range(1, 9):
            for j in range(1, 9):
                if (Board.colour_of_pos((i, j)) == Colour.WHITE and bturn == Colour.WHITE) or (
                        Board.colour_of_pos((i, j)) == Colour.BLACK and bturn == Colour.BLACK):
                    pygame.draw.rect(sc, ColoursRGB.CREAM,
                                     [(self.sqare_size + self.spaces) * i, (self.sqare_size + self.spaces) * (9 - j),
                                      self.sqare_size,
                                      self.sqare_size])
                else:
                    pygame.draw.rect(sc, ColoursRGB.BROWN,
                                     [(self.sqare_size + self.spaces) * i, (self.sqare_size + self.spaces) * (9 - j),
                                      self.sqare_size,
                                      self.sqare_size])
        if show_text:
            rendered = [[], []]
            for i in range(1, 9):
                if bturn == Colour.WHITE:
                    col = ColoursRGB.CREAM if i % 2 else ColoursRGB.BROWN
                    rendered[0].append(self.font.render(chr(ord("a") - 1 + i), True, col))
                    rendered[1].append(self.fontnum.render(str(i), True, col))
                else:
                    col = ColoursRGB.BROWN if i % 2 else ColoursRGB.CREAM
                    rendered[0].append(self.font.render(chr(ord("h") + 1 - i), True, col))
                    rendered[1].append(self.fontnum.render(str(9 - i), True, col))
            for i in range(1, 9):
                sc.blit(rendered[0][i - 1],
                        ((self.sqare_size + self.spaces) * (i + 1) - self.font_size + self.font_size / 3,
                         (self.sqare_size + self.spaces) * 9 - self.font_size - 5))
                sc.blit(rendered[1][i - 1],
                        ((self.sqare_size + self.spaces), (self.sqare_size + self.spaces) * (9 - i)))


a = Game("ChessGame", (1600, 900), 30)
a.run()
