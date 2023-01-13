from classes.Scene import Scene
from classes.RectW import RectW
from classes.TextInputW import TextInputW
from classes.TextW import TextW
from classes.ButtonW import ButtonW
from constants import *
from functions import *
from client import *


class Registration(Scene):
    def __init__(self):
        super().__init__()
        self.bg_color = ColoursRGB.LICHESS
        log_rect = RectW((*(self.bg_color * 1.8).rgb, 255), [RESOLUTION[0] // 2 - 250, RESOLUTION[1] // 2 - 200],
                         [500, 400], radius=50)

        self.pls_login = TextW("Регистрация", [30, 20], ColoursRGB.LIGHTGREY.rgb, ["arialblack", 40])
        self.email = TextInputW([35, 100], [430, 50], initial="Email:")
        self.email.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        log_text = get_param_from_client("regWithLog")

        self.log = TextInputW([35, 170], [430, 50], initial="Логин:")
        self.log.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        self.log.is_rgb = False

        if "@" in log_text:
            self.email.value = log_text
            self.email.textinput.value = log_text
            self.email.textinput_value = log_text
        else:
            self.log.value = log_text
            self.log.textinput.value = log_text
            self.log.textinput_value = log_text

        self.pas = TextInputW([35, 240], [430, 50], initial="Пароль:")
        self.pas.bg_color = (ColoursRGB.WHITE * 0.7).rgb
        pas_text = get_param_from_client("regWithPas")
        self.pas.value = pas_text
        self.pas.textinput.value = pas_text
        self.pas.textinput_value = pas_text

        but2 = ButtonW("Зарегистрироваться")
        but2.text_color = ColoursRGB.LIGHTGREY.rgb
        but2.set_font("arial", 40)
        but2.corner = [640, 583]
        but2.set_default_rect()
        but2.on_click(self.try_to_reg)
        but2.set_hover_bg_colour([*(self.bg_color * 2).rgb, 255])

        self.verdict = TextW("Неверный пароль", [690, 545], ColoursRGB.RED.rgb, ["arialblack", 20])
        log_rect.widgets.append("pls_login", self.pls_login, 1)
        log_rect.widgets.append("email", self.email, 1)
        log_rect.widgets.append("login", self.log, 1)
        log_rect.widgets.append("password", self.pas, 1)
        self.elements.append("verdict", self.verdict, 2)
        self.elements.append("reg_btn", but2, 2)
        self.elements.append("log_rect", log_rect, -1)

    def try_to_reg(self):
        email_text = self.email.get_text()
        log_text = self.log.get_text()
        pas_text = self.pas.get_text()
        verdict = registration(email_text, pas_text, log_text)
        print(verdict)
        if verdict == "Успешно":
            set_param_in_client("user", log_text)
            self.scene_manager.goto_scene("menu")

    def input_processing(self, events, events_p):
        super().input_processing(events, events_p)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.goto_scene("menu")

            if event.type == TIMER_EVENT_10TPS:
                email_text = self.email.get_text()
                log_text = self.log.get_text()
                pas_text = self.pas.get_text()
                verdict = try_to_registr(email_text, pas_text, log_text)
                if verdict == "Всё корректно":
                    self.verdict.color = ColoursRGB.GREEN.rgb
                    self.verdict.hover_text_color = ColoursRGB.GREEN.rgb
                    self.verdict.text_color = ColoursRGB.GREEN.rgb
                else:
                    self.verdict.color = ColoursRGB.RED.rgb
                    self.verdict.hover_text_color = ColoursRGB.RED.rgb
                    self.verdict.text_color = ColoursRGB.RED.rgb
                if self.verdict.text != verdict:
                    self.verdict.text = verdict

