from classes.Microphone import Microphone
from constants import *


class VoiceControl:
    def __init__(self, target_word):
        self.voice_control_word = target_word
        sl = {self.voice_control_word: self.activated}
        self.voice_control = Microphone(sl)
        self.clear_voice_control()

    def activated(self, x):
        with open(voice_path, "w") as f:
            f.write(x)

    def run(self):
        while True:
            self.voice_control.update()

    @staticmethod
    def is_move_request():
        try:
            with open(voice_path, "r") as f:
                a = f.readline().strip()
                return bool(a)
        except FileNotFoundError:
            return False

    @staticmethod
    def get_move_from_word_contol():
        with open(voice_path, "r") as f:
            return f.readline().strip()

    @staticmethod
    def clear_voice_control():
        with open(voice_path, "w") as f:
            f.write("")
