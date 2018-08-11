import pyxel
from globals import *
from util import *


class Drawable:
    def __init__(self):
        print("Created new ", self.__class__)
        self.elements = []

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self):
        for element in self.elements:
            element.draw()


class Blocks(Drawable):
    def __init__(self, env):
        super().__init__()

        self.env = env

    def draw(self):
        block_width = pyxel.width / GRID_HORIZONTAL_COUNT
        block_height = pyxel.height / GRID_VERTICAL_COUNT
        for y in range(GRID_VERTICAL_COUNT):
            for x in range(GRID_HORIZONTAL_COUNT):
                if (self.env.grid[y] >> (GRID_HORIZONTAL_COUNT - x - 1)) & 1:
                    pyxel.rect(x * block_width, y * block_height, (x + 1)
                               * block_width, (y + 1) * block_height, 7)


class Player(Drawable):
    def __init__(self, env):
        super().__init__()

        self.env = env

        block_width = pyxel.width / GRID_HORIZONTAL_COUNT
        block_height = pyxel.height / GRID_VERTICAL_COUNT

        self.height = block_height
        self.width = block_width
        self.x = 100
        self.y = 100

        self.v_vert = GRAVITY_VELOCITY_START
        self.v_hor = 0.0

    def heading_left(self):
        return self.v_hor < 0

    def heading_right(self):
        return self.v_hor > 0

    def update_move(self):
        if self.y == 0:
            if pyxel.btn(pyxel.KEY_D):
                self.v_hor = VELOCITY_MOVE

            if pyxel.btn(pyxel.KEY_A):
                self.v_hor = -VELOCITY_MOVE

        if self.v_hor != 0:
            self.x += self.v_hor

            if self.y == 0:
                self.v_hor *= FRICTION_DECELERATE

            if abs(self.v_hor) < 0.1:
                self.v_hor = 0.0

        if self.env.is_at_left(self.x, self.y, self.height) and self.heading_left():
            self.v_hor = 0
            self.x = self.env.left_for(self.x, self.y, self.height)
        elif self.env.is_at_right(self.x, self.y, self.width, self.height) and self.heading_right():
            self.v_hor = 0
            self.x = self.env.right_for(
                self.x, self.y, self.width, self.height) - self.width

    def update_jump(self):
        if self.env.is_at_bottom(self.x, self.y, self.width):
            if pyxel.btn(pyxel.KEY_SPACE):
                self.v_vert = 10

        if self.v_vert > 0:
            self.v_vert *= GRAVITY_DECELERATE
            if self.v_vert <= 1:
                self.v_vert = -0.1
        elif self.v_vert < 0:
            self.v_vert = max(VELOCITY_FALL_MAX, self.v_vert *
                              (1.0 + GRAVITY_DECELERATE))

        self.y += self.v_vert

        if self.env.is_at_bottom(self.x, self.y, self.width):
            self.y = self.env.bottom_for(self.x, self.y, self.width)
            self.v_vert = 0

    def update(self):
        self.update_move()
        self.update_jump()

    def draw(self):
        T.rect(self.x, self.y, self.width, self.height)
