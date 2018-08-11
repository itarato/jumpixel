import pyxel
from globals import *
from util import *


class Env:
    def __init__(self):
        self.grid = [
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000000,
            0b0000000001,
            0b1000000001,
            0b1100000111,
        ]

    def column_for(self, x):
        return int(x / T.block_width())

    def row_for(self, y):
        return int(y / T.block_height())

    def next_bottom_in_column(self, col, y):
        row = self.row_for(y + DISTANCE_ZERO_THRESHOLD)

        if row <= 0:
            return 0
        else:
            row_bottom = row - 1
            while row_bottom >= 0 and self.grid[GRID_VERTICAL_COUNT - 1 - row_bottom] == 0:
                row_bottom -= 1
            return row_bottom + 1

    def bottom_for(self, x, y, w):
        col_lhs = self.column_for(x)
        col_rhs = self.column_for(x + w)

        # print("COLLHS", col_lhs, "COLRHS", col_rhs)
        # print(self.row_for(y))

        row_bottom = self.next_bottom_in_column(col_lhs, y)

        if col_rhs != col_lhs:
            row_bottom = max(
                row_bottom, self.next_bottom_in_column(col_rhs, y))

        # print(row_bottom)

        return row_bottom * T.block_height()

    def is_at_bottom(self, x, y, w):
        return y - self.bottom_for(x, y, w) < DISTANCE_ZERO_THRESHOLD

    def left_for(self, x, y, h):
        return 0

    def is_at_left(self, x, y, h):
        return x - self.left_for(x, y, h) < DISTANCE_ZERO_THRESHOLD

    def right_for(self, x, y, w, h):
        return pyxel.width

    def is_at_right(self, x, y, w, h):
        return self.right_for(x, y, w, h) - (x + w) < DISTANCE_ZERO_THRESHOLD
