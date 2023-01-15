from classes.AnimationW import AnimationW
from classes.ButtonW import ButtonW
from classes.RectW import RectW
from classes.Scene import Scene
from classes.TextInputW import TextInputW
from classes.TextW import TextW
from client import vhod, get_client_name, razlogin
from functions import *


class SecondScene(Scene):
    def __init__(self):
        super().__init__()
        print("---menu_scene---")
        self.bg_color = ColoursRGB.LICHESS
        self._alredy_called_login = False
        self.playing_animation = False
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

        log_rect = RectW((*(self.bg_color * 1.8).rgb, 255), [1100, 300], [450, 300], radius=50)
        bg_decor_rect = RectW((*(self.bg_color * 1.8).rgb, 255), [300, 250], [700, 400], radius=50)

        self.log = TextInputW([35, 100], [380, 50], initial="Логин:")
        self.log.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        self.log.is_rgb = False

        self.pas = TextInputW([35, 170], [380, 50], initial="Пароль:")
        self.pas.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        self.pas.is_password = True
        self.pas.is_rgb = True

        self.log.on_value_changed(self._reset_alredy_called_login)
        self.pas.on_value_changed(self._reset_alredy_called_login)

        self.pls_login = TextW("Вход/Регистрация", [30, 20], ColoursRGB.LIGHTGREY.rgb, ["arialblack", 35])
        self.verdict1 = TextW("Неверный пароль", [20, 230], ColoursRGB.RED.rgb, ["arialblack", 20])
        self.verdict2 = TextW("Нажмите, чтобы зарегистрировать аккуант", [36, 240], ColoursRGB.RED.rgb,
                              ["arialblack", 15])

        self.verdict3 = TextW("User", [100, 10], ColoursRGB.LIGHTGREY.rgb,
                              ["arialblack", 70])

        self.verdict31 = TextW("Выйти", [50, 150], ColoursRGB.LIGHTGREY.rgb,
                               ["arialblack", 80])
        self.verdict31.on_click(self.unlogin)
        self.verdict31.hover_text_color = (ColoursRGB.LIGHTGREY * 1.8).rgb

        self.verdict2.hover_text_color = (ColoursRGB.RED * 0.7).rgb
        self.verdict2.on_click(self.go_to_register)
        self.verdict1.hide()
        self.verdict2.hide()
        self.verdict3.hide()
        self.verdict31.hide()
        path = create_full_path(r"/data/assets/animations/checkbox_alpha")

        self.anim = AnimationW(path, [70, 0], 300)
        log_rect.widgets.append("an", self.anim, 2)

        # log_rect.widgets.append("galochka", verdict3, 2)
        log_rect.widgets.append("unlogin", self.verdict31, 1)
        log_rect.widgets.append("user", self.verdict3, 1)
        log_rect.widgets.append("log_in_text", self.pls_login, 1)
        log_rect.widgets.append("verdict_wrong", self.verdict1, 1)
        log_rect.widgets.append("verdict_no_name", self.verdict2, 1)
        log_rect.widgets.append("login", self.log, 1)
        log_rect.widgets.append("password", self.pas, 1)
        self.elements.append("deco", bg_decor_rect, -1)
        self.elements.append("log_rect", log_rect, -1)
        self.elements.append("start_game_button", but, 0)
        self.elements.append("board_editor_button", but2, 0)

    def go_to_register(self):
        log = self.log.get_text()
        pas = self.pas.get_text()
        set_param_in_client("regWithLog", log)
        set_param_in_client("regWithPas", pas)
        self.scene_manager.goto_scene("register")

    def update(self):
        super().update()
        if get_client_name() != "None" and not self.playing_animation:
            self.show_loged_in()
        else:
            if self.log.get_text() and self.log.get_time_from_last_type() > 1 \
                    and self.pas.get_text() and self.pas.get_time_from_last_type() > 1 and not self._alredy_called_login:
                self._alredy_called_login = True
                log = self.log.get_text()
                pas = self.pas.get_text()
                verdict = vhod(log, pas)
                if verdict == "Успешно":
                    self.log.hide()
                    self.pas.hide()
                    self.pls_login.hide()
                    self.anim.play_cycle()
                    self.playing_animation = True

                if verdict == "Пароль неверный":
                    self.verdict1.show()
                if verdict == 'Пользователь не найден':
                    self.verdict2.show()
            if self.playing_animation and not self.anim.playing:
                self.show_loged_in()

    def show_loged_in(self):
        self.log.hide()
        self.pas.hide()
        self.pls_login.hide()
        self.playing_animation = False
        self.verdict3.show()
        if self.verdict3.text != get_client_name():
            self.verdict3.text = get_client_name()
        self.verdict31.show()

    def _reset_alredy_called_login(self):
        self.verdict1.hide()
        self.verdict2.hide()
        self._alredy_called_login = False

    def unlogin(self):
        razlogin()
        self.verdict3.hide()
        self.verdict3.text = get_client_name()
        self.verdict31.hide()
        self.log.show()
        self.log.value = ""
        self.log.selected = False
        self.log.textinput_value = self.log.inital
        self.pas.show()
        self.pas.value = ""
        self.pas.pass_input.value = ""
        self.pas.selected = False
        self.pas.textinput_value = self.pas.inital
        self.pls_login.show()