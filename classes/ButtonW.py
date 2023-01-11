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
        self.kwargs_["font"] = self._font

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
        self.button = Button(
            *self.args_,
            **self.kwargs_,
        )

    def on_click(self, func):
        self.kwargs_["onClick"] = func
        self.recreate()

    def on_click_params(self, params):
        self.kwargs_["onClickParams"] = params
        self.recreate()

    def disconnect_on_click(self):
        self.kwargs_["onClick"] = lambda: None
        if "onClickParams" in self.kwargs_:
            del self.kwargs_["onClickParams"]
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
        self.recreate()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect
        self.button.setWidth(rect[0])
        self.button.setHeight(rect[1])
        self.args_[3] = rect[0]
        self.args_[4] = rect[1]

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

    def enable(self):
        self.button.enable()

    def input_processing(self, events, events_p):
        mousepos = events_p[0]
        pressed_buttons = events_p[1]
        pressed_keys = events_p[2]
        dx, dy = events_p[3]
        self.mouse_coards = mousepos

    def draw(self, sc):
        sc.blit(self.surf, (0, 0))
