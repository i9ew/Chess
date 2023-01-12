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

        log = TextInputW([35, 100], [330, 50], initial="Логин:")
        log.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        log.is_rgb = True

        pas = TextInputW([35, 170], [330, 50], initial="Пароль:")
        pas.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        pas.is_password = True
        pas.is_rgb = True
        pas.on_clicked(lambda: print(f"Input: {pas.get_text()}"))
        pas.on_value_changed(lambda: print(pas.get_text()))

        pls_login = TextW("Вход", [30, 20], ColoursRGB.LIGHTGREY.rgb, ["arialblack", 40])
        verdict1 = TextW("Неправильный логин или пароль", [20, 230], ColoursRGB.RED.rgb, ["arialblack", 20])
        verdict2 = TextW("Нажмите, чтобы зарегистрировать аккуант", [20, 240], ColoursRGB.RED.rgb, ["arialblack", 15])
        verdict2.hover_text_color = (ColoursRGB.RED * 0.7).rgb
        verdict2.on_click(lambda: self.scene_manager.goto_scene("register"))
        verdict1.hide()
        verdict2.hide()
        path = create_full_path(r"/data/assets/animations/checkbox_alpha")
        print(path)
        a = AnimationW(path, [0, 0], 200)
        log_rect.widgets.append("an", a, 2)
        log.on_clicked(lambda: a.play_cycle())

        # log_rect.widgets.append("galochka", verdict3, 2)
        log_rect.widgets.append("log_in_text", pls_login, 1)
        log_rect.widgets.append("verdict_wrong", verdict1, 1)
        log_rect.widgets.append("verdict_no_name", verdict2, 1)
        log_rect.widgets.append("login", log, 1)
        log_rect.widgets.append("password", pas, 1)
        self.elements.append("log_rect", log_rect, -1)
        self.elements.append("start_game_button", but, 0)
        self.elements.append("board_editor_button", but2, 0)

    def check_login_and_password(self, login, password):
        pass
