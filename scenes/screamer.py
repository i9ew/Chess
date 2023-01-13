from classes.Scene import Scene
import pygame
from functions import *
from constants import *


class Screamer(Scene):
    def __init__(self):
        super().__init__()
        self.bg_color = ColoursRGB.RED
        self.bg_image_path = create_full_path(f"data/assets/images/screamer.png")

    def input_processing(self, events, events_p):
        super().input_processing(events, events_p)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.goto_scene("menu")
