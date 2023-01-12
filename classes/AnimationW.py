import os
from os import listdir

from functions import *


class AnimationW:
    def __init__(self, path_to_folder, corner, size):
        self.max_index = len(listdir(path_to_folder)) - 1
        self.start_from_frame = 3
        self.frame_index = self.start_from_frame
        self.corner = corner
        self.path_to_files = path_to_folder
        self.image = load_image(os.path.join(self.path_to_files, f"{self.frame_index}.png"))
        self.surf = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        self.size = size
        self._is_hidden = False
        self._play = False

    def hide(self):
        self._is_hidden = True

    def show(self):
        self._is_hidden = False

    def play_cycle(self):
        self.frame_index = self.start_from_frame
        self._play = True
        self.show()
        self.image = load_image(os.path.join(self.path_to_files, f"{self.frame_index}.png"))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def next_frame(self):
        if self.frame_index == self.start_from_frame - 1:
            self._play = False
            self.hide()
        if self._play:
            self.frame_index += 1
            if self.frame_index > self.max_index:
                self.frame_index = 0

            self.image = load_image(os.path.join(self.path_to_files, f"{self.frame_index}.png"))
            self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, sc):
        if not self._is_hidden:
            sc.blit(self.image, self.corner)

    def input_processing(self, events, events_p):
        if not self._is_hidden:
            mousepos = events_p[0]
            pressed_buttons = events_p[1]
            pressed_keys = events_p[2]
            dx, dy = events_p[3]
            for event in events:
                if event.type == TIMER_EVENT_20TPS:
                    self.next_frame()
