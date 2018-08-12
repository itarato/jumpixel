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


class BoundedElement():
    def __init__(self):
        self.height = 0
        self.width = 0
        self.x = 0
        self.y = 0


class Player(BoundedElement, Drawable):
    def __init__(self, env):
        super().__init__()

        self.env = env

        block_width = pyxel.width / GRID_HORIZONTAL_COUNT
        block_height = pyxel.height / GRID_VERTICAL_COUNT

        self.height = block_height - 4
        self.width = block_width - 4
        self.x = 100
        self.y = 100

        self.v_vert = GRAVITY_VELOCITY_START
        self.v_hor = 0.0

    def hmove_left(self):
        return self.v_hor < 0

    def hmove_right(self):
        return self.v_hor > 0

    def vmove_down(self):
        return self.v_vert < 0

    def vmove_up(self):
        return self.v_vert > 0

    def hmove_idle(self):
        return self.v_hor == 0

    def vmove_idle(self):
        return self.v_vert == 0

    def read_input(self):
        if self.env.is_at_bottom(self):
            move_velocity = VELOCITY_MOVE
        else:
            move_velocity = VELOCITY_MOVE_AIR

        if pyxel.btn(pyxel.KEY_D):
            self.v_hor = move_velocity

        if pyxel.btn(pyxel.KEY_A):
            self.v_hor = -move_velocity

        if self.env.is_at_bottom(self):
            if pyxel.btn(pyxel.KEY_W):
                self.v_vert = VELOCITY_JUMP

    def update_move(self):
        if self.v_hor != 0:
            next_left = self.env.left_for(self)
            next_right = self.env.right_for(self)

            if self.hmove_left and self.x + self.v_hor < next_left:
                self.x = next_left
            elif self.hmove_right and (self.x + self.width) + self.v_hor > next_right:
                self.x = next_right - self.width
            else:
                self.x += self.v_hor

            if self.env.is_at_bottom(self):
                self.v_hor *= FRICTION_DECELERATE

            if abs(self.v_hor) < 0.1:
                self.v_hor = 0.0

        if self.env.is_at_left(self) and self.hmove_left():
            self.v_hor = 0
            self.x = self.env.left_for(self)
        elif self.env.is_at_right(self) and self.hmove_right():
            self.v_hor = 0
            self.x = self.env.right_for(self) - self.width

    def update_jump(self):
        if self.v_vert > 0:
            self.v_vert *= GRAVITY_DECELERATE
            if self.v_vert <= 1:
                self.v_vert = -0.1
        elif self.v_vert < 0:
            self.v_vert = max(VELOCITY_FALL_MAX, self.v_vert *
                              (1.0 + GRAVITY_DECELERATE))

        next_bottom = self.env.bottom_for(self)

        if self.vmove_down and next_bottom > self.y + self.v_vert:
            self.y = next_bottom
        else:
            self.y += self.v_vert

        if self.env.is_at_bottom(self):
            self.y = self.env.bottom_for(self)
            self.v_vert = 0

    def update_fall(self):
        if self.vmove_idle() and not self.env.is_at_bottom(self):
            self.v_vert = -GRAVITY_VELOCITY_START

    def update(self):
        self.read_input()
        self.update_move()
        self.update_jump()
        self.update_fall()

    def draw(self):
        T.rect(self.x, self.y, self.width, self.height)
