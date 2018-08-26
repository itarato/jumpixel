from random import random
from globals import *


class Map:
    def __init__(self, w, h):
        self.map = [ENV_FOOD * w] * h
        self.w = w
        self.h = h

    def generate(self):
        for y in range(2, self.h - 1, 2):
            pos = 0
            toggle_type_is_ground = True
            while pos < self.w:
                len = int(random() * self.w / 2)
                while len > 0 and pos < self.w:
                    if toggle_type_is_ground:
                        self.__update_grid(pos, y, ENV_GROUND)

                    pos += 1
                    len -= 1

                    if random() > 0.6:
                        self.__update_grid(pos, y - 1, ENV_FOOD)

                toggle_type_is_ground = not toggle_type_is_ground

        self.__update_grid(int(self.w / 2), self.h - 1, ENV_PLAYER)
        return self.map

    def is_cell(self, col, row, type):
        col = min(max(0, col), self.w - 1)
        row = min(max(0, row), self.h - 1)
        return self.map[self.h - 1 - row][col] == type

    def player_pos(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.is_cell(x, y, ENV_PLAYER):
                    return (x, y)

        return (0, 0)

    def __update_grid(self, x, y, type):
        self.map[y] = self.map[y][:x] + type + self.map[y][x + 1:]
