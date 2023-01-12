import pygame_textinput

from functions import *
from time import time


class TextInputW:
    def __init__(self, corner, rect, initial=""):
        self.rect_ = rect
        self.corner = corner
        self.font = pygame.font.SysFont("arial", int(self.rect[1] * 0.9))
        self.value = ""
        self.inital = initial
        self.manager = pygame_textinput.TextInputManager(
            validator=lambda inp: self._add_text(inp))
        self.pasmanager = pygame_textinput.TextInputManager(
            validator=lambda inp: self._add_text(inp))
        self.textinput = pygame_textinput.TextInputVisualizer(manager=self.manager)
        self.pass_input = None
        self.surf = pygame.Surface(self.rect, pygame.SRCALPHA)
        self.bg_color = (0, 0, 0, 0)
        self.textinput.font_object = self.font
        self.value = ""
        self.is_password_ = False
        self._call_from_pass_input = False
        self.textinput_value = None
        self.is_rgb_ = False
        self._value_states = [self.inital, self.inital]
        self.functions = {}
        self._is_hidden = False
        self.text_color = [0, 0, 0, 255]
        self.rgb_text_color = [0, 85, 170]
        self.selected = False
        self.last_time_typed = time()

    def hide(self):
        self._is_hidden = True

    def show(self):
        self._is_hidden = False

    @property
    def is_rgb(self):
        return self.is_rgb_

    @is_rgb.setter
    def is_rgb(self, value):
        if value and not self.is_rgb_:
            self.is_rgb_ = value
        elif not value and self.is_rgb_:
            self.is_rgb_ = value
            self.textinput.font_color = self.text_color

    @property
    def is_password(self):
        return self.is_password_

    @is_password.setter
    def is_password(self, value):
        self.is_password_ = value
        if self.is_password_:
            self.pass_input = pygame_textinput.TextInputVisualizer(manager=self.pasmanager)
        else:
            self.pass_input = None

    def is_in_box(self, text):
        return self.font.size(text)[0] < self.rect[0]

    def _add_text(self, text):
        self.textinput_value = None
        if not self._call_from_pass_input:
            if self.is_password:
                self.textinput_value = "*" * len(self.pass_input.value)
                return False
            else:
                t = text
                is_in_box = self.is_in_box(t)
                if is_in_box:
                    self.value = text
                    self.textinput_value = text
                return False
        else:
            t = "*" * len(text)
            is_in_box = self.is_in_box(t)
            self.value = text
            return is_in_box

    def get_time_from_last_type(self):
        return time() - self.last_time_typed

    @property
    def rect(self):
        return self.rect_

    @rect.setter
    def rect(self, value):
        self.rect_ = value
        self.font = pygame.font.SysFont("arial", self.rect[1])

    def on_clicked(self, func):
        self.functions["onClicked"] = func

    def on_clicked_params(self, func):
        self.functions["onClickedParams"] = func

    def disconnect_on_clicked(self):
        if "onClicked" in self.functions:
            del self.functions["onClicked"]
        if "onClickedParams" in self.functions:
            del self.functions["onClickedParams"]

    def _on_clicked_process(self):
        if "onClicked" in self.functions:
            if "onClickedParams" in self.functions:
                self.functions["onClicked"](*self.functions["onClickedParams"])
            else:
                self.functions["onClicked"]()

    def on_value_changed(self, func):
        self.functions["onValueChanged"] = func

    def on_value_changed_params(self, func):
        self.functions["onValueChangedParams"] = func

    def disconnect_on_value_changed(self):
        if "onValueChanged" in self.functions:
            del self.functions["onValueChanged"]
        if "onValueChangedParams" in self.functions:
            del self.functions["onValueChangedParams"]

    def _on_value_changed_process(self):
        self.last_time_typed = time()
        if "onValueChanged" in self.functions:
            if "onValueChangedParams" in self.functions:
                self.functions["onValueChanged"](*self.functions["onValueChangedParams"])
            else:
                self.functions["onValueChanged"]()

    @property
    def value_changed(self):
        return self._value_states[0] != self._value_states[1]

    def _value_change_catch(self, value):
        self._value_states = [value, self._value_states[0]]

    def select_processing(self, events, events_p):
        mousepos = events_p[0]
        pressed_buttons = events_p[1]
        pressed_keys = events_p[2]
        dx, dy = events_p[3]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.selected = mouse_in_rect(mousepos, self.rect, self.corner)

    def input_processing(self, events, events_p):
        mousepos = events_p[0]
        pressed_buttons = events_p[1]
        pressed_keys = events_p[2]
        dx, dy = events_p[3]
        self.select_processing(events, events_p)
        if not self._is_hidden and self.selected:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self._on_clicked_process()
                if event.type == pygame.KEYDOWN:
                    if not self.value:
                        self.textinput.value = ""

            if self.pass_input is not None:
                self._call_from_pass_input = True
                self.pass_input.update(events)
                self._call_from_pass_input = False
                self.value = self.pass_input.value
            self.textinput.update(events)
            if self.textinput_value is not None:
                self.textinput.value = self.textinput_value
                self.manager.cursor_pos = len(self.textinput.value)

            self._value_change_catch(self.value)
            if self.value_changed:
                self._on_value_changed_process()
        if not self._is_hidden:
            if not self.value:
                self.textinput.value = self.inital

            for event in events:
                if event.type == TIMER_EVENT_20TPS:
                    if not self.value:
                        self.textinput.font_color = self.text_color
                    elif self.is_rgb:
                        self.textinput.font_color = [(c + 10) % 255 for c in self.rgb_text_color]
                        self.rgb_text_color = self.textinput.font_color

        if not self.selected:
            self.textinput.cursor_visible = False
            self.textinput.font_color = self.text_color
        else:
            self.textinput.cursor_blink_interval = 400
            if self.is_rgb and self.value:
                self.textinput.font_color = self.rgb_text_color

    def get_text(self):
        return self.value

    @property
    def text(self):
        return self.value

    @text.setter
    def text(self, value):
        self.value = value
        self.textinput.value = value

    def draw(self, screen):
        if not self._is_hidden:
            self.surf.fill(self.bg_color)
            self.surf.blit(self.textinput.surface, [0, 0])
            screen.blit(self.surf, self.corner)
