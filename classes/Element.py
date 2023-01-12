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

    def disable(self):
        for el in self:
            if "disable" in dir(el):
                el.disable()

    def update(self):
        for el in self:
            if "update" in dir(el):
                el.update()

    def render(self, screen):
        for el in self:
            if "draw" in dir(el):
                el.draw(screen)

    def input_processing(self, events, events_p):
        for el in self:
            if "input_processing" in dir(el):
                el.input_processing(events, events_p)