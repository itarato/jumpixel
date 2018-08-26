from random import random


class Map:
    def __init__(self, w, h):
        self.map = ['0' * w] * h
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
                        self.__update_grid(pos, y, '1')

                    pos += 1
                    len -= 1

                    if random() > 0.6:
                        self.__update_grid(pos, y - 1, '2')

                toggle_type_is_ground = not toggle_type_is_ground

        self.__update_grid(int(self.w / 2), self.h - 1, '9')
        return self.map

    def __update_grid(self, x, y, type):
        self.map[y] = self.map[y][:x] + type + self.map[y][x + 1:]
