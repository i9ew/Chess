import sys

from constants import *


def classname(clas):
    return clas.__class__.__name__


def load_image(path, colorkey=None):
    # fullname = os.path.join('data', name)
    fullname = path
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_figure(figure: str):
    from classes.figures.Bishop import Bishop
    from classes.figures.King import King
    from classes.figures.Knight import Knight
    from classes.figures.Pawn import Pawn
    from classes.figures.Queen import Queen
    from classes.figures.Rook import Rook
    sl = {
        "K": King,
        "R": Rook,
        "N": Knight,
        "B": Bishop,
        "P": Pawn,
        "Q": Queen

    }
    try:
        if figure.isupper():
            return [sl[figure], Chess.WHITE_FIGURE]
        else:
            return [sl[figure.upper()], Chess.BLACK_FIGURE]
    except KeyError:
        raise KeyError(f"There is no such figure in chess '{figure}'")


def set_param_in_client(param, value):
    try:
        with open(user_path, 'r') as f:
            a = f.readlines()
    except:
        a = []
    with open(user_path, 'w') as f:
        flag = False
        for i in range(len(a)):
            if a[i].split("=")[0] == param:
                flag = True
                a[i] = f"{param}={value}"
            a[i] = a[i].strip()
        if not flag:
            a.append(f"{param}={value}")
        f.writelines("\n".join(a))


def get_param_from_client(param):
    try:
        with open(user_path, 'r') as f:
            a = f.readlines()
            for i in range(len(a)):
                if a[i].split("=")[0] == param:
                    return a[i].split("=")[1].strip()
    except:
        return None


def clear_client():
    with open(user_path, 'w') as f:
        f.write("")


def import_figures():
    from classes.figures.Pawn import Pawn
    from classes.figures.King import King
    from classes.figures.Queen import Queen
    from classes.figures.Knight import Knight
    from classes.figures.Rook import Rook
    from classes.figures.Bishop import Bishop
    figures = King, Queen, Rook, Bishop, Knight, Pawn
    return figures


def create_full_path(path):
    splited_p = path.split("/")
    if hasattr(sys, "_MEIPASS") and FILES_ARE_SAVING_TO_APPDATA:
        return os.path.join(sys._MEIPASS, *splited_p)
    return os.path.join(*splited_p)


def coards_to_indexes(coards):
    sl = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }
    return [sl[coards[0]], 8 - int(coards[1])]


def get_text_rect(text, font):
    # font = pygame.font.SysFont(font_name, size_of_font)
    text = font.render(
        text, True, (255, 255, 255))
    text_rect = text.get_rect()
    return text_rect


def mouse_in_rect(mousecoards, rect, corner):
    return inRange(corner, mousecoards, [corner[0] + rect[0], corner[1] + rect[1]])


def indexes_to_coards(indexes):
    sl = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h"
    }
    return str(sl[indexes[0]]) + str(8 - int(indexes[1]))


def inRange(mi, x, ma):
    ans = [mi[i] <= x[i] <= ma[i] for i in range(len(min(mi, ma, x, key=lambda x: len(x))))]
    return all(ans)
