import pygame
class Scene:

    def __init__(self):
        self.next_scene = None
        self.elements = {}

    def input_processing(self, events):
        for el in self.elements.values():
            try:
                el.input_processing(events)
            except:
                pass

    def update(self):
        for el in self.elements.values():
            try:
                el.update()
            except:
                pass

    def render(self, screen):
        for el in self.elements.values():
            try:
                el.draw(screen)
            except:
                pass

    @property
    def next(self):
        return self.next_scene
