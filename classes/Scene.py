class Scene:

    def __init__(self):
        self.next_scene = None
        self.elements = {}
        self.error_protection = False

    def input_processing(self, events, events_p):
        for el in self.elements.values():
            if self.error_protection:
                try:
                    el.input_processing(events, events_p)
                # except AttributeError:
                #     pass
                except Exception as err:
                    print(err)
            else:
                el.input_processing(events, events_p)

    def update(self):
        for el in self.elements.values():
            if self.error_protection:
                try:
                    el.update()
                # except AttributeError:
                #     pass
                except Exception as err:
                    print(err)
            else:
                el.update()

    def render(self, screen):
        for el in self.elements.values():
            if self.error_protection:
                try:
                    el.draw(screen)
                # except AttributeError:
                #     pass
                except Exception as err:
                    print(err)
            else:
                el.draw(screen)

    @property
    def next(self):
        return self.next_scene
