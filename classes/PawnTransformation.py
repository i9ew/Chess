from classes.figures.Bishop import Bishop
from classes.figures.Knight import Knight
from classes.figures.Queen import Queen
from classes.figures.Rook import Rook
from functions import *


class PawnTransformation:
    def __init__(self, color, theme, sqare_size, corner, from_sqare="", to_square=""):
        self.b_sqare_size = sqare_size
        self.b_corner = corner
        self.color = color
        self.theme = theme
        self.figures = pygame.sprite.Group()
        self.corner = [self.b_corner[0], self.b_corner[1] + self.b_sqare_size * 3]
        self.rect = [self.b_sqare_size * 8, self.b_sqare_size * 2]
        self.draw_color = self.theme["primary_color"]
        # self.draw_color = self.draw_color[0] * 2 // 3, self.draw_color[1] * 2 // 3, self.draw_color[2] * 2 // 3
        self.draw_color = self.draw_color * (2 / 3)
        self.figs = [Bishop, Knight, Rook, Queen]
        c = 0
        for fig in self.figs:
            fig = fig(self.figures, self.theme, self.color)
            fig.set_coards([self.corner[0] + self.b_sqare_size * 2 * c, self.corner[1]])
            fig.set_size(self.b_sqare_size * 2)
            c += 1
        self.is_active = False
        self.move = [from_sqare, to_square]

    def input_processing(self, events, events_p):
        if self.is_active:
            mousepos = events_p[0]
            pressed_buttons = events_p[1]
            pressed_keys = events_p[2]
            dx, dy = events_p[3]
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        if self.get_figure(mousepos):
                            return self.move[0], self.move[1] + self.get_figure(mousepos)
                        else:
                            return False

    def get_figure(self, coards):
        if inRange(self.corner, coards, [self.corner[0] + self.rect[0], self.corner[1] + self.rect[1]]):
            index = (coards[0] - self.corner[0]) // (self.b_sqare_size * 2)
            sl = {
                0: str(self.figs[0](None, self.theme, self.color)),
                1: str(self.figs[1](None, self.theme, self.color)),
                2: str(self.figs[2](None, self.theme, self.color)),
                3: str(self.figs[3](None, self.theme, self.color)),
            }
            return sl[index]
        return False

    def draw(self, sc):
        if self.is_active:
            surf = pygame.Surface(self.rect)
            surf.fill(self.draw_color.rgb)
            sc.blit(surf, self.corner)
            self.figures.draw(sc)
