import pygame

from constants import *


class EvaluationW:
    def __init__(self, rect, corner):
        self.surf = pygame.Surface(rect, pygame.SRCALPHA)
        self.rect = rect
        self.corner = corner
        self.draw_k = 0.5
        self.evaluation = None
        self.is_hidden = False
        self.c1 = ColoursRGB.WHITE.rgb
        self.c2 = ColoursRGB.BLACK.rgb
        self.game_ = None

    def game_eval(self, game):
        if game.evaluation:
            self.evaluation = game.evaluation
            value = self.evaluation['value']
            if self.evaluation['type'] == 'cp':
                self.c1 = ColoursRGB.WHITE.rgb
                self.c2 = ColoursRGB.BLACK.rgb
                self.set_draw_k_from_evaluation(value / 100)
            elif self.evaluation['type'] == 'mate':
                if self.evaluation['value'] > 0:
                    self.c1 = ColoursRGB.WHITE.rgb
                    self.c2 = ColoursRGB.WHITE.rgb
                    self.set_draw_k_from_evaluation(5)
                elif self.evaluation['value'] < 0:
                    self.c1 = ColoursRGB.BLACK.rgb
                    self.c2 = ColoursRGB.BLACK.rgb
                    self.set_draw_k_from_evaluation(-5)

    @property
    def game(self):
        return self.game_

    @game.setter
    def game(self, g):
        self.game_ = g
        self.game_eval(g)

    def set_draw_k_from_evaluation(self, val):
        if val > 5:
            val = 5
        if val < -5:
            val = -5
        self.draw_k = (val + 5) / 10

    def hide(self):
        self.is_hidden = True

    def show(self):
        self.is_hidden = False

    def draw(self, sc):
        if not self.is_hidden:
            pygame.draw.rect(self.surf, self.c1,
                             pygame.Rect(0, self.rect[1] - self.rect[0], self.rect[0], self.rect[0]),
                             border_radius=self.rect[0] // 4)
            pygame.draw.rect(self.surf, self.c2,
                             pygame.Rect(0, 0, self.rect[0], self.rect[0]),
                             border_radius=self.rect[0] // 4)

            pygame.draw.rect(self.surf, ColoursRGB.WHITE.rgb,
                             pygame.Rect(0, self.rect[0] // 2, self.rect[0],
                                         self.rect[1] - self.rect[0]))

            pygame.draw.rect(self.surf, ColoursRGB.BLACK.rgb,
                             pygame.Rect(0, self.rect[0] // 2, self.rect[0],
                                         (self.rect[1] - self.rect[0]) * (1 - self.draw_k)))

            sc.blit(self.surf, self.corner)

    def update(self):
        if self.game is not None:
            self.game_eval(self.game)

    def input_processing(self, events, events_p):
        pass
