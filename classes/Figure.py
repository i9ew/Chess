from functions import *


class Figure(pygame.sprite.Sprite):
    def __init__(self, group, theme, color, placement="", image_path=""):
        self.group = group
        if group is not None:
            super().__init__(group)
        self.color = color
        if type(theme) is dict:
            self.style = theme["figure_style"]
        else:
            self.style = theme
        self.direct_image_path = image_path
        if image_path == "":
            self.letter = self.get_figure_letter()
            self.image_path = self.get_figure_path()
        else:
            self.image_path = image_path
        self.image = load_image(self.image_path)
        self.rect = self.image.get_rect()
        self.placement = placement
        self.coards = [50, 50]
        self.rect.x = self.coards[0]
        self.rect.y = self.coards[1]
        self.size = self.rect.size[0]

        self.select_k = 1.3
        self._selected = False
        self._is_sprite_to_track_mouse = False

        self._draw_ghoul = False
        self._draw_bigger = False

    @property
    def is_sprite_to_track_mouse(self):
        return self._is_sprite_to_track_mouse

    @is_sprite_to_track_mouse.setter
    def is_sprite_to_track_mouse(self, value):
        self._is_sprite_to_track_mouse = value
        if value:
            self.draw_bigger = 1.2

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected and not value:
            # print(f"Unselected {classname(self)} on {self.placement}")
            self.draw_bigger = False
            self.draw_ghoul = False

        if not self._selected and value:
            # print(f"Selected {classname(self)} on {self.placement}")'
            self.draw_bigger = True
            # self.image.set_alpha(50)

        self._selected = value

    @property
    def draw_bigger(self):
        return self._draw_bigger

    @draw_bigger.setter
    def draw_bigger(self, value):
        if value:
            im = load_image(self.image_path)
            if type(value) is bool:
                self.image = pygame.transform.scale(im,
                                                    (int(self.size * self.select_k), int(self.size * self.select_k)))
            else:
                self.image = pygame.transform.scale(im,
                                                    (int(self.size * value), int(self.size * value)))
            self.rect.x -= self.size * (self.select_k - 1) // 2
            self.rect.y -= self.size * (self.select_k - 1) // 2
        else:
            im = load_image(self.image_path)
            self.image = pygame.transform.scale(im, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x = self.coards[0]
            self.rect.y = self.coards[1]

    @property
    def draw_ghoul(self):
        return self._draw_ghoul

    @draw_ghoul.setter
    def draw_ghoul(self, val):
        if val:
            self.image.set_alpha(50)
        else:
            self.image.set_alpha(255)

    def copy_with_no_group(self):
        return Figure(None, self.style, self.color, self.placement, image_path=self.image_path)

    def refresh_theme(self):
        if self.direct_image_path == "":
            self.image_path = self.get_figure_path()
        self.image = load_image(self.image_path)

    def get_figure_path(self):
        return create_full_path(rf"/data/assets/figure_styles/{self.style}/{'w' if self.color == Chess.WHITE_FIGURE else 'b'}{self.letter}.png")

    def set_coards(self, coards):
        self.coards = coards
        self.rect.x = self.coards[0]
        self.rect.y = self.coards[1]

    def calculate_coards(self, corner, sqare_size, isreversed):
        indexes = coards_to_indexes(self.placement)
        coards_on_screen = [indexes[0] * sqare_size,
                            indexes[1] * sqare_size]
        if isreversed:
            coards_on_screen = [7 * sqare_size - coards_on_screen[0], 7 * sqare_size - coards_on_screen[1]]

        coards_on_screen = [coards_on_screen[0] + corner[0], coards_on_screen[1] + corner[1]]

        self.set_coards(coards_on_screen)
        self.set_size(sqare_size)

    def set_size(self, size):
        im = load_image(self.image_path)
        self.image = pygame.transform.scale(im, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = self.coards[0]
        self.rect.y = self.coards[1]
        self.size = self.rect.size[0]

    def select(self):
        self.selected = True

    def get_figure_letter(self):
        sl = {
            "King": "K",
            "Rook": "R",
            "Knight": "N",
            "Pawn": "P",
            "Bishop": "B",
            "Queen": "Q"

        }
        try:
            if self.color == Chess.WHITE_FIGURE:
                return sl[self.__class__.__name__]
            else:
                return sl[self.__class__.__name__].lower()
        except KeyError:
            raise KeyError(f"There is no such figure in chess '{self.__class__.__name__}'")

    def __str__(self):
        return self.letter

    def __repr__(self):
        return self.__class__.__name__
