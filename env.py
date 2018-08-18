import pyxel
from globals import *
from util import *
from ui import *
from events import *


class Env:
    def __init__(self):
        self.grid = [
            0b00000000,
            0b11110000,
            0b00000010,
            0b00000000,
            0b10000100,
            0b00011001,
            0b10000001,
            0b11000111,
        ]

        self.food = [
            0b11110000,
            0b00000010,
            0b00100100,
            0b10000100,
            0b00011001,
            0b10000000,
            0b01000110,
            0b00111000,
        ]

        self.eventloop = EventLoop()

    def is_ground(self, col, row):
        return T.is_grid_cell_on(self.grid, col, row)

    def is_food(self, col, row):
        return T.is_grid_cell_on(self.food, col, row)

    def look_for_food(self, eater: BoundedElement):
        # for food in self.
        pass

    def column_for(self, x):
        return int(x / T.block_width())

    def row_for(self, y):
        return int(y / T.block_height())

    def next_bottom_in_column(self, col, y):
        row = self.row_for(y + DISTANCE_ZERO_THRESHOLD)

        if row <= 0:
            return 0
        else:
            row_current = row - 1
            while row_current >= 0 and not self.is_ground(col, row_current):
                row_current -= 1
            return row_current + 1

    def next_left_in_row(self, row, x):
        col = self.column_for(x + DISTANCE_ZERO_THRESHOLD)

        if col <= 0:
            return 0
        else:
            col_current = col - 1
            while col_current >= 0 and not self.is_ground(col_current, row):
                col_current -= 1
            return col_current + 1

    def next_right_in_row(self, row, x):
        col = self.column_for(x - DISTANCE_ZERO_THRESHOLD)

        if col >= GRID_HORIZONTAL_COUNT - 1:
            return GRID_HORIZONTAL_COUNT
        else:
            col_current = col + 1
            while col_current < GRID_VERTICAL_COUNT and not self.is_ground(col_current, row):
                col_current += 1
            return col_current

    def bottom_for(self, e: BoundedElement):
        col_lhs = self.column_for(e.x + DISTANCE_ZERO_THRESHOLD)
        col_rhs = self.column_for(e.x + e.width - DISTANCE_ZERO_THRESHOLD)

        row_bottom = self.next_bottom_in_column(col_lhs, e.y)
        row_bottom = max(row_bottom, self.next_bottom_in_column(col_rhs, e.y))

        return row_bottom * T.block_height() + 1

    def is_at_bottom(self, e: BoundedElement):
        return e.y - self.bottom_for(e) < DISTANCE_ZERO_THRESHOLD

    def left_for(self, e: BoundedElement):
        row_bottom = self.row_for(e.y)
        row_top = self.row_for(e.y + e.height)

        col_left = self.next_left_in_row(row_bottom, e.x)
        col_left = max(col_left, self.next_left_in_row(row_top, e.x))

        return col_left * T.block_width()

    def is_at_left(self, e: BoundedElement):
        return e.x - self.left_for(e) < DISTANCE_ZERO_THRESHOLD

    def right_for(self, e: BoundedElement):
        row_bottom = self.row_for(e.y)
        row_top = self.row_for(e.y + e.height)

        col_right = self.next_right_in_row(row_bottom, e.x + e.width)
        col_right = max(col_right, self.next_right_in_row(
            row_top, e.x + e.width))

        return col_right * T.block_width() - 1

    def is_at_right(self, e: BoundedElement):
        return self.right_for(e) - (e.x + e.width) < DISTANCE_ZERO_THRESHOLD
