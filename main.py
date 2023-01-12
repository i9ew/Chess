import pygame
import pygame_widgets as pw

from classes.SceneManeger import SceneManeger
from constants import *
from scenes.main_scene import MainScene
from scenes.second_scene import SecondScene
from scenes.board_editor import BoardEditor
from scenes.registration import Registration
from client import *


class Game:
    def __init__(self, name, size, FPS):
        pygame.init()
        pygame.mixer.init()
        self.name = name
        self.size = size
        self.FPS = FPS

    def run(self):
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.name)
        clock = pygame.time.Clock()
        running = True
        scenes = {"game": MainScene, "menu": SecondScene, "board_editor": BoardEditor, "register": Registration}
        scene_manager = SceneManeger(scenes)
        scene_manager.goto_scene("menu")
        dx = dy = 0
        start = (0, 0)
        mousepos = (0, 0)

        pygame.time.set_timer(TIMER_EVENT_10TPS, 1000 // 10)
        pygame.time.set_timer(TIMER_EVENT_20TPS, 1000 // 20)

        while running:
            screen.fill(ColoursRGB.BLACK.rgb)
            events = pygame.event.get()
            pressed_keys = pygame.key.get_pressed()
            pressed_buttons = pygame.mouse.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    clear_client()
                    razlogin()
                    # sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = event.pos
                    dx = dy = 0
                    start = mousepos
                if event.type == pygame.MOUSEMOTION:
                    mousepos = event.pos
                    dx, dy = mousepos[0] - start[0], mousepos[1] - start[1]

            scene_manager.process_scene(screen, events, [mousepos, pressed_buttons, pressed_keys, [dx, dy]])
            pygame.display.update()
            pw.update(events)
            clock.tick(self.FPS)


if __name__ == "__main__":
    a = Game(NAME, RESOLUTION, FPS)
    a.run()
