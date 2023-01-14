import pygame
from functions import *
from classes.Element import Elements


class RectW:
    def __init__(self, color, corner, rect, radius=0):
        self.color = color
        self.corner = corner
        self.rect = rect
        self.surf = pygame.Surface(self.rect, pygame.SRCALPHA)
        self.radius = radius
        self._is_hidden = False
        self.widgets = Elements()
        self.bg_image = None
        self.bg_image_path = None

    def hide(self):
        self._is_hidden = True

    def show(self):
        self._is_hidden = False

    def draw(self, screen):
        if not self._is_hidden:
            pygame.draw.rect(self.surf, self.color,
                             pygame.Rect(0, 0, self.rect[0], self.rect[1]),
                             border_radius=self.radius)
            if self.bg_image is not None:
                screen.blit(self.bg_image, (0, 0))
            self.widgets.render(self.surf)
            screen.blit(self.surf, self.corner)

    def input_processing(self, events, events_p):
        w_events_p = events_p.copy()
        w_events_p[0] = [w_events_p[0][0] - self.corner[0], w_events_p[0][1] - self.corner[1]]
        if not self._is_hidden:
            self.widgets.input_processing(events, w_events_p)

    def update(self):
        if self.bg_image_path is not None:
            im = load_image(self.bg_image_path)
            self.bg_image = pygame.transform.scale(im, RESOLUTION)
        if not self._is_hidden:
            self.widgets.update()

    def disable(self):
        self.widgets.disable()
