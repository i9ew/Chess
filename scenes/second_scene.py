from classes.AnimationW import AnimationW
from classes.ButtonW import ButtonW
from classes.RectW import RectW
from classes.Scene import Scene
from classes.TextInputW import TextInputW
from classes.TextW import TextW
from functions import *


class SecondScene(Scene):
    def __init__(self):
        super().__init__()
        print("---menu_scene---")
        self.bg_color = ColoursRGB.LICHESS
        self._alredy_called_login = False
        but = ButtonW("Начать игру")
        but.text_color = ColoursRGB.LIGHTGREY.rgb
        but.set_inactive_bg_colour((*(self.bg_color * 1.8).rgb, 255))
        but.set_hover_bg_colour((*(self.bg_color * 2).rgb, 255))
        but.on_click(lambda: self.scene_manager.goto_scene("game"))
        but.rect = [300, 300]
        but.corner = [(RESOLUTION[0] - but.rect[0]) // 2 - 300, (RESOLUTION[1] - but.rect[1]) // 2]

        but2 = ButtonW("Редактор доски")
        but2.text_color = ColoursRGB.LIGHTGREY.rgb
        but2.set_font("arial", 40)
        but2.set_inactive_bg_colour((*(self.bg_color * 1.8).rgb, 255))
        but2.set_hover_bg_colour((*(self.bg_color * 2).rgb, 255))
        but2.on_click(lambda: self.scene_manager.goto_scene("board_editor"))
        but2.rect = [300, 300]
        but2.corner = [(RESOLUTION[0] - but2.rect[0]) // 2, (RESOLUTION[1] - but2.rect[1]) // 2]

        log_rect = RectW((*(self.bg_color * 1.8).rgb, 255), [1100, 50], [400, 300], radius=50)

        self.log = TextInputW([35, 100], [330, 50], initial="Логин:")
        self.log.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        self.log.is_rgb = True

        self.pas = TextInputW([35, 170], [330, 50], initial="Пароль:")
        self.pas.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        self.pas.is_password = True
        self.pas.is_rgb = True

        self.log.on_value_changed(self._reset_alredy_called_login)
        self.pas.on_value_changed(self._reset_alredy_called_login)

        pls_login = TextW("Вход", [30, 20], ColoursRGB.LIGHTGREY.rgb, ["arialblack", 40])
        self.verdict1 = TextW("Неправильный логин или пароль", [20, 230], ColoursRGB.RED.rgb, ["arialblack", 20])
        self.verdict2 = TextW("Нажмите, чтобы зарегистрировать аккуант", [20, 240], ColoursRGB.RED.rgb,
                              ["arialblack", 15])
        self.verdict2.hover_text_color = (ColoursRGB.RED * 0.7).rgb
        self.verdict2.on_click(lambda: self.scene_manager.goto_scene("register"))
        self.verdict1.hide()
        self.verdict2.hide()
        path = create_full_path(r"/data/assets/animations/checkbox_alpha")
        self.anim = AnimationW(path, [40, 0], 300)
        log_rect.widgets.append("an", self.anim, 2)

        # log_rect.widgets.append("galochka", verdict3, 2)
        log_rect.widgets.append("log_in_text", pls_login, 1)
        log_rect.widgets.append("verdict_wrong", self.verdict1, 1)
        log_rect.widgets.append("verdict_no_name", self.verdict2, 1)
        log_rect.widgets.append("login", self.log, 1)
        log_rect.widgets.append("password", self.pas, 1)
        self.elements.append("log_rect", log_rect, -1)
        self.elements.append("start_game_button", but, 0)
        self.elements.append("board_editor_button", but2, 0)

    def update(self):
        if self.log.get_text() and self.log.get_time_from_last_type() > 1 \
                and self.pas.get_text() and self.pas.get_time_from_last_type() > 1 and not self._alredy_called_login:
            print(f"log: {self.log.get_text()}, pas: {self.pas.get_text()}")
            self._alredy_called_login = True
            if self.log.get_text() == "Максим":
                self.anim.play_cycle()

    def _reset_alredy_called_login(self):
        self._alredy_called_login = False
