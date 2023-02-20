from classes.ButtonW import ButtonW
from classes.RectW import RectW
from classes.TextW import TextW
from classes.figures.King import King
from constants import *
import pygame


class EndGameWidget:
    def __init__(self, board_corner, square_size, theme):
        self.turn = Chess.WHITE_FIGURE
        self.verdict = 1

        self.square_size = square_size
        self.board_rect = [square_size * 8, square_size * 8]
        self.surf = pygame.Surface(self.board_rect, pygame.SRCALPHA)
        self.corner = board_corner
        self.is_hidden = False
        self.bg_rect = RectW((*ColoursRGB.BLACK.rgb, 150), [0, 0], self.board_rect)
        self.theme = theme

        self.tcorner = [self.square_size * 1.75, self.square_size * 1.75]
        self.end_game_rect = RectW((*ColoursRGB.DARKGREY.rgb, 255), self.tcorner,
                                   [self.square_size * 4.5, self.square_size * 4.5], radius=60)
        self.text_name_turn = TextW(("Белые" if self.turn == Chess.WHITE_FIGURE else "Чёрные"),
                                    [self.tcorner[0] + self.square_size, self.tcorner[1] + 50],
                                    (ColoursRGB.WHITE.rgb if self.turn == Chess.WHITE_FIGURE else ColoursRGB.BLACK.rgb),
                                    ["arialblack", 50])
        self.text2 = TextW("победили", [self.text_name_turn.corner[0] - 20, self.text_name_turn.corner[1] + 70],
                           ColoursRGB.LIGHTGREY.rgb, ["arialblack", 50])
        self.figures = pygame.sprite.Group()
        self.king = King(self.figures, self.theme, self.turn)
        self.king.set_size(self.square_size * 2)
        self.king.set_coards(
            [self.text2.corner[0] + 50, self.text2.corner[1] + 90])

    def show(self):
        self.is_hidden = False

    def hide(self):
        self.is_hidden = True

    def set_verdict(self, verdict):
        self.verdict = verdict
        if verdict != 0:
            self.turn = Chess.WHITE_FIGURE if verdict == 1 else Chess.BLACK_FIGURE
            self.tcorner = [self.square_size * 1.75, self.square_size * 1.75]
            self.end_game_rect = RectW((*ColoursRGB.DARKGREY.rgb, 255), self.tcorner,
                                       [self.square_size * 4.5, self.square_size * 4.5], radius=60)
            self.text_name_turn = TextW(("Белые" if self.turn == Chess.WHITE_FIGURE else "Чёрные"),
                                        [self.tcorner[0] + self.square_size, self.tcorner[1] + 50],
                                        (
                                            ColoursRGB.WHITE.rgb if self.turn == Chess.WHITE_FIGURE else ColoursRGB.BLACK.rgb),
                                        ["arialblack", 50])
            self.text2 = TextW("победили", [self.text_name_turn.corner[0] - 20, self.text_name_turn.corner[1] + 70],
                               ColoursRGB.LIGHTGREY.rgb, ["arialblack", 50])
            self.figures = pygame.sprite.Group()
            self.king = King(self.figures, self.theme, self.turn)
            self.king.set_size(self.square_size * 2)
            self.king.set_coards(
                [self.text2.corner[0] + 50, self.text2.corner[1] + 90])
        else:
            self.tcorner = [self.square_size * 2, self.square_size * 3]
            self.end_game_rect = RectW((*ColoursRGB.DARKGREY.rgb, 255), self.tcorner,
                                       [self.square_size * 4, self.square_size * 2], radius=60)
            self.text2 = TextW("Ничья", [self.tcorner[0] + self.square_size // 2, self.tcorner[1] + self.square_size // 2 - 10],
                               ColoursRGB.LIGHTGREY.rgb, ["arialblack", 80])

    def draw(self, sc):
        self.surf.fill([0, 0, 0, 0])
        if not self.is_hidden:
            self.bg_rect.draw(self.surf)
            self.end_game_rect.draw(self.surf)
            if self.verdict in [-1, 1]:
                self.text_name_turn.draw(self.surf)
                self.figures.draw(self.surf)
                self.text2.draw(self.surf)
            else:
                self.text2.draw(self.surf)

        sc.blit(self.surf, self.corner)

    def update(self):
        self.text_name_turn.update()
        self.text2.update()
