from functions import *
from constants import *


class Scene:
    def __init__(self):
        self.next_scene = None
        self.elements = {}
        self.error_protection = False
        self.scene_manager = None
        self.bg_image_path = None
        self.bg_image = None

    def input_processing(self, events, events_p):
        for el in self.elements.values():
            if self.error_protection:
                try:
                    el.input_processing(events, events_p)
                except AttributeError:
                    pass
                except Exception as err:
                    raise err
            else:
                el.input_processing(events, events_p)

    def update(self):
        for el in self.elements.values():
            if self.error_protection:
                try:
                    el.update()
                except AttributeError:
                    pass
                except Exception as err:
                    raise err
            else:
                el.update()
        if self.bg_image_path is not None:
            im = load_image(self.bg_image_path)
            self.bg_image = pygame.transform.scale(im, RESOLUTION)

    def render(self, screen):
        if self.bg_image is not None:
            screen.blit(self.bg_image, (0, 0))
        for el in self.elements.values():
            if self.error_protection:
                try:
                    el.draw(screen)
                except AttributeError:
                    pass
                except Exception as err:
                    raise err
            else:
                el.draw(screen)

    @property
    def next(self):
        return self.next_scene
