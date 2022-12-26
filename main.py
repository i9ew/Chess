import pygame

from classes.SceneManeger import SceneManeger
from constants import *
from scenes.main_scene import MainScene



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
        scenes = {"main": MainScene}
        scene_manager = SceneManeger(scenes)
        while running:
            screen.fill(ColoursRGB.BLACK)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    # sys.exit()
                if event.type == pygame.KEYDOWN:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = event.pos
            scene_manager.process_scene(screen, events)
            pygame.display.update()
            clock.tick(self.FPS)


if __name__ == "__main__":
    a = Game(NAME, RESOLUTION, FPS)
    a.run()
