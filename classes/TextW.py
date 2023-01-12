from classes.ButtonW import ButtonW


class TextW(ButtonW):
    def __init__(self, text, corner, color, font):
        super().__init__(text)
        self.corner = corner
        self.set_font(*font)
        self.text_color = color
