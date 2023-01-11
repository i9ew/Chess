from functions import *


class Elements:
    def __init__(self):
        self.layers = {0: {}}

    def append(self, name, el, layer):
        other = [el, name, layer]
        if other[2] in self.layers:
            self.layers[other[2]][other[1]] = other[0]
        else:
            self.layers[other[2]] = {other[1]: other[0]}

    def __getitem__(self, ln):
        layer, name = ln
        return self.layers[layer][name]

    def __iter__(self):
        for layer in sorted(self.layers):
            for el in self.layers[layer].values():
                yield el


class Scene:
    def __init__(self):
        self.next_scene = None
        self.elements = Elements()
        self.error_protection = False
        self.scene_manager = None
        self.bg_image_path = None
        self.bg_image = None
        self.bg_color = None

    def input_processing(self, events, events_p):
        for el in self.elements:
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
        for el in self.elements:
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
        if self.bg_color is not None:
            screen.fill(self.bg_color.rgb)
        if self.bg_image is not None:
            screen.blit(self.bg_image, (0, 0))
        for el in self.elements:
            if self.error_protection:
                try:
                    el.draw(screen)
                except AttributeError:
                    pass
                except Exception as err:
                    raise err
            else:
                el.draw(screen)

    def disable(self):
        for el in self.elements:
            if self.error_protection:
                try:
                    el.disable()
                except AttributeError:
                    pass
                except Exception as err:
                    raise err
            else:
                el.disable()

    @property
    def next(self):
        return self.next_scene
