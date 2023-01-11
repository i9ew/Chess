from classes.ButtonW import ButtonW
from classes.Scene import Scene
from constants import *


class SecondScene(Scene):
    def __init__(self):
        super().__init__()
        print("---menu_scene---")
        self.bg_color = ColoursRGB.LICHESS2
        but = ButtonW("Начать игру")
        but.text_color = (255, 255, 255, 255)
        but.set_inactive_bg_colour((*(self.bg_color * 1.2).rgb, 255))
        but.set_hover_bg_colour((*(self.bg_color * 1.3).rgb, 255))
        but.on_click(lambda: self.scene_manager.goto_scene("game"))
        but.rect = [300, 300]
        but.corner = [(RESOLUTION[0] - but.rect[0]) // 2 - 300, (RESOLUTION[1] - but.rect[1]) // 2]

        but2 = ButtonW("Редактор доски")
        but2.text_color = (255, 255, 255, 255)
        but2.set_font("arial", 40)
        but2.set_inactive_bg_colour((*(self.bg_color * 1.2).rgb, 255))
        but2.set_hover_bg_colour((*(self.bg_color * 1.3).rgb, 255))
        but2.on_click(lambda: self.scene_manager.goto_scene("board_editor"))
        but2.rect = [300, 300]
        but2.corner = [(RESOLUTION[0] - but2.rect[0]) // 2, (RESOLUTION[1] - but2.rect[1]) // 2]

        self.elements.append("start_game_button", but, 0)
        self.elements.append("board_editor_button", but2, 0)
