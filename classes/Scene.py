class Scene:
    def __init__(self):
        self.next_scene = None

    def input_processing(self, events):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass

    @property
    def next(self):
        return self.next_scene
