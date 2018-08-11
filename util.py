import pyxel
from globals import *


class T:
    @staticmethod
    def rect(x, y, w, h, c=11):
        pyxel.rect(x, pyxel.height - y, x + w, pyxel.height - y - h, c)

    @staticmethod
    def block_width():
        return pyxel.width / GRID_VERTICAL_COUNT

    @staticmethod
    def block_height():
        return pyxel.height / GRID_HORIZONTAL_COUNT
