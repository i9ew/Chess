from functions import *
from classes.Element import Elements



class Scene:
    def __init__(self):
        self.next_scene = None
        self.elements = Elements()
        self.scene_manager = None
        self.bg_image_path = None
        self.bg_image = None
        self.bg_color = None

    def input_processing(self, events, events_p):
        self.elements.input_processing(events, events_p)

    def update(self):
        self.elements.update()
        if self.bg_image_path is not None:
            im = load_image(self.bg_image_path)
            self.bg_image = pygame.transform.scale(im, RESOLUTION)

    def render(self, screen):
        if self.bg_color is not None:
            screen.fill(self.bg_color.rgb)
        if self.bg_image is not None:
            screen.blit(self.bg_image, (0, 0))
        for el in self.elements:
            if "draw" in dir(el):
                el.draw(screen)

    def disable(self):
        for el in self.elements:
            if "disable" in dir(el):
                el.disable()

    @property
    def next(self):
        return self.next_scene
