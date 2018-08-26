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

    @staticmethod
    def is_grid_cell_on(grid, col, row, type):
        col = min(max(0, col), GRID_HORIZONTAL_COUNT - 1)
        row = min(max(0, row), GRID_VERTICAL_COUNT - 1)
        return grid[GRID_VERTICAL_COUNT - 1 - row][col] == type
