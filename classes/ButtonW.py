import pygame
from pygame_widgets.button import Button

from functions import *


class ButtonW:
    def __init__(self, text, ar=None, kw=None, ad=None):
        if ad is None:
            ad = {}
        self.surf = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        self.mouse_coards = [0, 0]
        self._corner = [0, 0]
        self._bg_size = [0, 0]
        self.font_name = "arial"
        self._font = pygame.font.SysFont("arial", 50)
        self._rect = get_text_rect(text, self.font)[2:]
        self.ad = ad
        self.hover_st = [False, False]
        self.args_ = [
            self.surf,  # Surface to place button on
            self._corner[0],  # X-coordinate of top left corner
            self._corner[1],  # Y-coordinate of top left corner
            self.rect[0],  # Width
            self.rect[1],  # Height
        ]
        self.kwargs_ = {
            "text": text,
            "margin": 20,
            "inactiveColour": (0, 0, 0, 0),
            "hoverColour": (0, 0, 0, 0),
            "pressedColour": (0, 0, 0, 0),
            "radius": 0,
            "onClick": lambda: None,
            "font": self.font,
            "textColour": (255, 255, 255, 255),
            "onClickParams": [],
        }
        self._text_color = self.kwargs_["textColour"]
        self._text_hover_color = self.kwargs_["hoverColour"]
        if ar is not None:
            self.args_ = ar
        if kw is not None:
            self.kwargs_ = kw

        self.button = Button(
            *self.args_,
            **self.kwargs_,
        )
        self._is_hidden = False
        self._is_disabled = False

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self.recreate()

    @property
    def text(self):
        return self.kwargs_["text"]

    @text.setter
    def text(self, value):
        self.kwargs_["text"] = value
        self.recreate()

    def set_font(self, name, size):
        self._font = pygame.font.SysFont(name, size)
        # new_rect = get_text_rect(self.kwargs_["text"], self.font)[2:]
        self.set_default_rect()
        self.kwargs_["font"] = self._font
        self.kwargs_["fontSize"] = size
        # self.corner = [self.corner[0]]
        self.recreate()

    def set_inactive_bg_colour(self, val):
        self.kwargs_["inactiveColour"] = val
        self.recreate()

    def set_hover_bg_colour(self, val):
        self.kwargs_["hoverColour"] = val
        self.recreate()

    def set_pressed_bg_colour(self, val):
        self.kwargs_["pressedColour"] = val
        self.recreate()

    def set_rect_bigger_in_x_times(self, x):
        self.rect = [self.rect[0] * x, self.rect[1] * x]

    def recreate(self):
        self.surf = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        self.args_[0] = self.surf
        self.button.disable()
        self.button = Button(
            *self.args_,
            **self.kwargs_,
        )

    def on_click(self, func):
        self.ad["onClick"] = func
        self.recreate()

    def on_click_params(self, params):
        self.ad["onClickParams"] = params
        self.recreate()

    def disconnect_on_click(self):
        self.ad["onClick"] = lambda: None
        if "onClickParams" in self.ad:
            del self.ad["onClickParams"]
        self.recreate()

    def on_hover(self, func):
        self.ad["onHover"] = func
        self.recreate()

    def on_hover_params(self, params):
        self.ad["onHoverParams"] = params
        self.recreate()

    def disconnect_on_hover(self):
        self.kwargs_["onHover"] = lambda: None
        if "onHoverParams" in self.ad:
            del self.ad["onHoverParams"]
        self.recreate()

    def on_dishover(self, func):
        self.ad["onDishover"] = func
        self.recreate()

    def on_dishover_params(self, params):
        self.ad["onDishoverParams"] = params
        self.recreate()

    def disconnect_on_dishover(self):
        self.kwargs_["onDishover"] = lambda: None
        if "onDishoverParams" in self.ad:
            del self.ad["onDishoverParams"]
        self.recreate()

    @property
    def corner(self):
        return self._corner

    @corner.setter
    def corner(self, value):
        self.args_[1] = value[0]
        self.args_[2] = value[1]
        self._corner = [value[0], value[1]]
        self.recreate()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect
        self.button.setWidth(self._rect[0])
        self.button.setHeight(self._rect[1])
        self.args_[3] = self._rect[0]
        self.args_[4] = self._rect[1]

    def set_default_rect(self):
        self.rect = get_text_rect(self.kwargs_["text"], self.font)[2:]

    @property
    def draw_text_color(self):
        return self.button.textColour

    @draw_text_color.setter
    def draw_text_color(self, val):
        self.kwargs_["textColour"] = val
        self.recreate()

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value
        if self.hover_text_color == (0, 0, 0, 0):
            self.hover_text_color = value

    @property
    def hover_text_color(self):
        return self._text_hover_color

    @hover_text_color.setter
    def hover_text_color(self, val):
        self._text_hover_color = val

    @property
    def is_hover(self):
        return self.button.contains(self.mouse_coards[0], self.mouse_coards[1])

    def set_arg(self, arg, value):
        self.kwargs_[arg] = value
        self.recreate()

    def update(self):
        self.hover_st = [self.is_hover, self.hover_st[0]]
        if self.is_hover and self.draw_text_color != self.hover_text_color:
            self.draw_text_color = self.hover_text_color
        elif not self.is_hover and self.draw_text_color != self.text_color:
            self.draw_text_color = self.text_color

        if self.hover_st == [True, False] and "onHover" in self.ad:
            if "onHoverParams" in self.ad:
                self.ad["onHover"](*self.ad["onHoverParams"])
            else:
                self.ad["onHover"]()
        if self.hover_st == [False, True] and "onDishover" in self.ad:
            if "onDishoverParams" in self.ad:
                self.ad["onDishover"](*self.ad["onDishoverParams"])
            else:
                self.ad["onDishover"]()

    def disable(self):
        self.button.disable()
        self._is_disabled = True

    def enable(self):
        self.button.enable()
        self._is_disabled = True

    def hide(self):
        self._is_hidden = True
        # self.button.hide()

    def show(self):
        self._is_hidden = False
        # self.button.show()

    def input_processing(self, events, events_p):
        mousepos = events_p[0]
        pressed_buttons = events_p[1]
        pressed_keys = events_p[2]
        dx, dy = events_p[3]
        if not self._is_disabled and not self._is_hidden:
            self.mouse_coards = mousepos
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT and self.is_hover:
                        if "onClick" in self.ad:
                            if "onClickParams" in self.ad:
                                self.ad["onClick"](*self.ad["onClickParams"])
                            else:
                                self.ad["onClick"]()

    def draw(self, sc):
        if not self._is_hidden:
            sc.blit(self.surf, (0, 0))
