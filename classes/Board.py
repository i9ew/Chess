from __future__ import annotations

from classes.FEN import FEN
from classes.HUDobjects import *
from classes.PawnTransformation import PawnTransformation


class Board:
    def __init__(self):
        self.history = []
        self.hud = HUDobjects()
        self.position = [[" " for __ in range(8)] for __ in range(8)]
        self._board_size = 720
        self.sqare_size = self.board_size // 8
        self._theme = {"primary_color": ColoursRGB.BROWN,
                       "secondary_color": ColoursRGB.CREAM,
                       "figure_style": "alpha",
                       "hud1": [ColoursRGB.GREEN, 150]}
        self._corner = [0, 0]
        self._game = None
        self.figures = pygame.sprite.Group()

        self.font_size = self.board_size // 28
        self.fontnum_size = self.board_size // 30
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.fontnum = pygame.font.SysFont("arial", self.fontnum_size)
        self.isreversed = False
        self.selected_sprite_to_track = None

        self.pawn_transformation_table = PawnTransformation(Chess.WHITE_FIGURE, self.theme, self.sqare_size,
                                                            self.corner)
        self.watch_mode = False

        self.board_moving = None

    def update(self):
        pass

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, game):
        self.set_FEN_position(game.FEN_position)
        game.play_on_boards.append(self)
        self._game = game

    def draw(self, sc):
        self.draw_board(sc, Chess.BLACK_FIGURE if self.isreversed else Chess.WHITE_FIGURE)
        self.figures.draw(sc)
        if self.get_selected():
            # self.draw_possible_moves(sc, self.get_selected().placement)
            self.hud.draw(sc)

        if self.selected_sprite_to_track is not None:
            image = self.selected_sprite_to_track.image
            coards = self.selected_sprite_to_track.rect
            sc.blit(image, coards)
        if not self.watch_mode:
            self.pawn_transformation_table.draw(sc)

    def add_to_hud_possible_moves(self, from_sqare):
        if self.game:
            moves = self.game.all_possible_moves_from(from_sqare)
            for sqare in moves:
                if self.is_sqare_empty(sqare):
                    CircleInSqare(self.hud, self.theme["hud1"][0], self.theme["hud1"][1], sqare, self.sqare_size // 5)
                else:
                    TrianglesInSqare(self.hud, self.theme["hud1"][0], self.theme["hud1"][1], sqare,
                                     self.sqare_size // 4)
            self.hud.calculate_corners(self.corner, self.sqare_size, self.isreversed)

    def pawn_transformation_processing(self, events, events_p):
        ans = None
        if self.pawn_transformation_table.is_active:
            ans = self.pawn_transformation_table.input_processing(events, events_p)
            if ans:
                self.make_move(from_sqare=ans[0], to_square=ans[1])
                self.pawn_transformation_table.is_active = False
            elif ans == Chess.INCORRECT_MOVE:
                self.unselect_all()
                self.pawn_transformation_table.is_active = False
        return ans

    def move_processing(self, events, events_p):
        mousepos = events_p[0]
        pressed_buttons = events_p[1]
        pressed_keys = events_p[2]
        dx, dy = events_p[3]
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.game:
                        self.game.pop_history()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coards_on_board = self.get_mouse_coards_on_board(mousepos)
                    if coards_on_board:
                        square = self.get_sqare_from_board_coards(coards_on_board)
                        moved = False
                        if self.get_selected():
                            to_square = square
                            from_sqare = self.get_selected().placement
                            moved = self.make_move(from_sqare, to_square)
                        if not moved:
                            if not self.is_sqare_empty(square) and self.get_from_sqare(square):
                                flag = True
                                if self.game:
                                    fig = self.get_from_sqare(square)
                                    if fig.color != self.game.turn:
                                        flag = False
                                if flag:
                                    self.select_figure(square)
                                else:
                                    self.unselect_all()
                            else:

                                self.unselect_all()

                    else:

                        self.unselect_all()
            if event.type == pygame.MOUSEMOTION:
                if pressed_buttons[pygame.BUTTON_LEFT - 1] and (abs(dx) > 3 or abs(dy) > 3):
                    selected = self.get_selected()
                    if selected:
                        selected.draw_bigger = False
                        selected.draw_ghoul = True
                        self.selected_sprite_to_track = selected.copy_with_no_group()
                        self.selected_sprite_to_track.is_sprite_to_track_mouse = True
                        self.selected_sprite_to_track.rect.x = max(
                            min(selected.rect.x + dx, self.corner[0] + self.sqare_size * 7),
                            self.corner[0] - self.sqare_size // 3)
                        self.selected_sprite_to_track.rect.y = max(
                            min(selected.rect.y + dy, self.corner[1] + self.sqare_size * 7),
                            self.corner[1] - self.sqare_size // 3)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if abs(dx) > 3 or abs(dy) > 3:
                        coards_on_board = self.get_mouse_coards_on_board(mousepos)
                        if coards_on_board:
                            if self.selected_sprite_to_track:
                                to_square = self.get_sqare_from_board_coards(coards_on_board)
                                from_sqare = self.selected_sprite_to_track.placement
                                if to_square and to_square != from_sqare:
                                    self.make_move(from_sqare, to_square)

                        self.unselect_all()
                    if self.get_selected():
                        self.get_selected().draw_ghoul = False
                    self.selected_sprite_to_track = None

    def input_processing(self, events, events_p):
        mousepos = events_p[0]
        pressed_buttons = events_p[1]
        pressed_keys = events_p[2]
        dx, dy = events_p[3]
        self.move_board(events, events_p)
        if not self.watch_mode:
            ans = self.pawn_transformation_processing(events, events_p)
            if ans is None:
                self.move_processing(events, events_p)
        for event in events:
            if event.type == pygame.KEYDOWN and self.get_mouse_coards_on_board(mousepos):
                if event.key == pygame.K_e:
                    self.isreversed = not self.isreversed
                if event.key == pygame.K_h:
                    if self.game:
                        print(*self.game.moves_history)

    def move_board(self, events, events_p):
        mousepos = events_p[0]
        pressed_buttons = events_p[1]
        pressed_keys = events_p[2]
        dx, dy = events_p[3]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.get_mouse_coards_on_board(mousepos):
                if event.button == pygame.BUTTON_RIGHT:
                    self.board_moving = self.corner
                    self.unselect_all()

            if event.type == pygame.MOUSEMOTION:
                if pressed_buttons[pygame.BUTTON_RIGHT - 1]:
                    if self.board_moving:
                        self.corner = [self.board_moving[0] + dx, self.board_moving[1] + dy]

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_RIGHT:
                    self.board_moving = None

    def make_move(self, from_sqare, to_square):
        if self.game:
            res = self.game.move_request(from_sqare, to_square)
            if res in [Chess.PAWN_TRANSFORMATION_WHITE, Chess.PAWN_TRANSFORMATION_BLACK]:
                self.pawn_transformation_table = PawnTransformation(Chess.WHITE_FIGURE, self.theme, self.sqare_size,
                                                                    self.corner, from_sqare=from_sqare,
                                                                    to_square=to_square)
                self.pawn_transformation_table.is_active = True
            return res

    def get_selected(self):
        for fig in self.figures:
            if fig.selected:
                return fig
        return None

    def get_from_sqare(self, sqare):
        for fig in self.figures:
            if fig.placement == sqare:
                return fig
        return None

    def is_sqare_empty(self, sqare):
        for fig in self.figures:
            if fig.placement == sqare:
                return False
        return True

    def get_mouse_coards_on_board(self, mouse_pos):
        if inRange(self.corner, mouse_pos,
                   [self.corner[0] + self.sqare_size * 8, self.corner[1] + self.sqare_size * 8]):
            return [mouse_pos[0] - self.corner[0], mouse_pos[1] - self.corner[1]]
        return None

    def get_sqare_from_board_coards(self, coards_on_board):
        indexes = [coards_on_board[0] // self.sqare_size, coards_on_board[1] // self.sqare_size]
        if self.isreversed:
            indexes = [7 - indexes[0], 7 - indexes[1]]
        return indexes_to_coards(indexes)

    def unselect_all(self):
        self.selected_sprite_to_track = None
        for fig in self.figures:
            if fig.selected:
                fig.selected = False

    def select_figure(self, coards):
        self.hud.clear()
        self.add_to_hud_possible_moves(coards)
        for fig in self.figures:
            if fig.placement == coards and not fig.selected:
                self.unselect_all()
                fig.select()

    def draw_board(self, sc, turn):
        for i in range(1, 9):
            for j in range(1, 9):
                color = self.theme["primary_color" if ((j + i + 1) % 2) else "secondary_color"]
                pygame.draw.rect(sc, color.rgb,
                                 [self.sqare_size * (i - 1) + self.corner[0],
                                  self.sqare_size * (8 - j) + self.corner[1],
                                  self.sqare_size,
                                  self.sqare_size])

        rendered = [[], []]
        for i in range(1, 9):
            col = self.theme["secondary_color" if i % 2 else "primary_color"].rgb
            if turn == Chess.WHITE_FIGURE:
                rendered[0].append(self.font.render(chr(ord("a") - 1 + i), True, col))
                rendered[1].append(self.fontnum.render(str(9 - i), True, col))
            else:
                rendered[0].append(self.font.render(chr(ord("h") + 1 - i), True, col))
                rendered[1].append(self.fontnum.render(str(i), True, col))
        for i in range(1, 9):
            sc.blit(rendered[0][i - 1],
                    (self.sqare_size * (i - 1) + self.corner[0],
                     self.sqare_size * 8 + self.corner[1] - self.font_size - 3 * self.board_size // 720))
            sc.blit(rendered[1][i - 1],
                    (self.sqare_size * 8 + self.corner[0] - self.fontnum_size + 10 * self.board_size // 720,
                     self.sqare_size * (i - 1) + self.corner[1]))

    @property
    def isreversed(self):
        return self._isreversed

    @isreversed.setter
    def isreversed(self, val):
        self._isreversed = val
        for fig in self.figures:
            fig.calculate_coards(self.corner, self.sqare_size, self.isreversed)
        self.hud.calculate_corners(self.corner, self.sqare_size, self.isreversed)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        self._theme = value
        for fig in self.figures:
            fig.style = self._theme["figure_style"]
            fig.refresh_theme()

    @property
    def board_size(self):
        return self._board_size

    @board_size.setter
    def board_size(self, value):
        self._board_size = value
        self.sqare_size = self.board_size // 8
        self.font_size = self.board_size // 28
        self.fontnum_size = self.board_size // 30
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.fontnum = pygame.font.SysFont("arial", self.fontnum_size)
        for fig in self.figures:
            indexes = coards_to_indexes(fig.placement)
            coards_on_screen = [self.corner[0] + indexes[0] * self.sqare_size,
                                self.corner[1] + indexes[1] * self.sqare_size]
            fig.set_coards(coards_on_screen)
            fig.set_size(self.sqare_size)
        self.hud.calculate_corners(self.corner, self.sqare_size, self.isreversed)

    @property
    def corner(self):
        return self._corner

    @corner.setter
    def corner(self, value):
        self._corner = value
        for fig in self.figures:
            indexes = coards_to_indexes(fig.placement)
            coards_on_screen = [self.corner[0] + indexes[0] * self.sqare_size,
                                self.corner[1] + indexes[1] * self.sqare_size]
            fig.set_coards(coards_on_screen)
        self.hud.calculate_corners(self.corner, self.sqare_size, self.isreversed)

    def set_position(self, position, history=None):
        self.position = position
        if history is not None:
            self.history = history

    def clear_board(self, history=False):
        if history:
            self.history = []
        self.position = [[" " for __ in range(8)] for __ in range(8)]
        self.figures = pygame.sprite.Group()

    def set_FEN_position(self, FEN_position):
        position = FEN(FEN_position).position
        self.clear_board()
        for i in position:
            self.place_figure(i[0], i[2], i[1])
        self.isreversed = not self.isreversed
        self.isreversed = not self.isreversed

    def place_figure(self, figure, coards, color):
        fig = figure(self.figures, self.theme, color, placement=coards)
        indexes = coards_to_indexes(coards)
        self.position[indexes[1]][indexes[0]] = fig.letter
        # indexes = coards_to_indexes(fig.placement)
        # coards_on_screen = [self.corner[0] + indexes[0] * self.sqare_size,
        #                     self.corner[1] + indexes[1] * self.sqare_size]
        # fig.set_coards(coards_on_screen)
        # fig.set_size(self.sqare_size)
        fig.calculate_coards(self.corner, self.sqare_size, False)

    def __str__(self):
        ans = "\n"
        if self.game:
            number_of_move = FEN(self.game.FEN_position).move_number
            ans += f"- Move number {number_of_move} -\n"
        else:
            ans += "-" * 10 + "\n"
        for i in self.position:
            for j in i:
                ans += str(j) + ' '
            ans += "\n"

        ans += "White: "
        buf = []
        for i in self.figures:
            if i.color == Chess.WHITE_FIGURE:
                buf.append(str(i).upper() + i.placement)
        ans += ", ".join(sorted(buf, key=lambda x: (["K", "Q", "R", "B", "N", "P"].index(x[0]), x[1:]))).replace("P",
                                                                                                                 "")
        ans += "\nBlack: "
        buf = []
        for i in self.figures:
            if i.color == Chess.BLACK_FIGURE:
                buf.append(str(i).upper() + i.placement)
        ans += ", ".join(sorted(buf, key=lambda x: (["K", "Q", "R", "B", "N", "P"].index(x[0]), x[1:]))).replace("P",
                                                                                                                 "")
        ans += "\n" + "-" * 10 + "\n"
        return ans
