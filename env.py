import pyxel
from globals import *
from util import *
from ui import *


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

    def is_grid_ground(self, col, row):
        return self.grid[GRID_VERTICAL_COUNT - 1 - col] >> (GRID_HORIZONTAL_COUNT - 1 - row) & 1 == 1

    def column_for(self, x):
        return int(x / T.block_width())

    def row_for(self, y):
        return int(y / T.block_height())

    def next_bottom_in_column(self, col, y):
        row = self.row_for(y + DISTANCE_ZERO_THRESHOLD)

        print("NEXTBOTROW", y, "=", row)

        if row <= 0:
            return 0
        else:
            row_current = row - 1
            while row_current >= 0 and not self.is_grid_ground(col, row_current):
                row_current -= 1
            return row_current + 1

    def bottom_for(self, e: BoundedElement):
        col_lhs = self.column_for(e.x)
        col_rhs = self.column_for(e.x + e.width)

        # print("COLLHS", col_lhs, "COLRHS", col_rhs)
        # print(self.row_for(y))

        row_bottom = self.next_bottom_in_column(col_lhs, e.y)

        if col_rhs != col_lhs:
            row_bottom = max(
                row_bottom, self.next_bottom_in_column(col_rhs, e.y))

        # print("ROWBTM", row_bottom)

        return row_bottom * T.block_height()

    def is_at_bottom(self, e: BoundedElement):
        return e.y - self.bottom_for(e) < DISTANCE_ZERO_THRESHOLD

    def left_for(self, e: BoundedElement):
        return 0

    def is_at_left(self, e: BoundedElement):
        return e.x - self.left_for(e) < DISTANCE_ZERO_THRESHOLD

    def right_for(self, e: BoundedElement):
        return pyxel.width

    def is_at_right(self, e: BoundedElement):
        return self.right_for(e) - (e.x + e.width) < DISTANCE_ZERO_THRESHOLD
