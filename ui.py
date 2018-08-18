import pyxel
from globals import *
from util import *


DIR_LEFT = 0
DIR_RIGHT = 1


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
                               * block_width - 1, (y + 1) * block_height - 1, 3)


class BoundedElement():
    def __init__(self):
        self.height = 0
        self.width = 0
        self.x = 0
        self.y = 0

    def x2(self):
        return self.x + self.width - 1

    def y2(self):
        return self.y + self.height - 1

    def is_cover(self, rhs):
        return (self.x <= rhs.x2()) and (self.x2() >= rhs.x) and (self.y <= rhs.y2()) and (self.y2() >= rhs.y)


class Food(Drawable, BoundedElement):
    def __init__(self, x, y):
        super().__init__()
        self.height = 8
        self.width = 8
        self.x = x
        self.y = y

    def draw(self):
        T.rect(self.x, self.y, self.width, self.height, c=4)


class Foods(Drawable):
    def __init__(self, env):
        super().__init__()

        self.env = env
        self.foods = []
        self.init_food()

        self.env.eventloop.sub(EVENT_EAT_TRY, self.check_eating)

    def check_eating(self, eater: BoundedElement):
        for food in self.foods:
            if food.is_cover(eater):
                self.foods.remove(food)
                self.elements.remove(food)
                self.env.eventloop.send(EVENT_EAT_SUCCESS)

    def init_food(self):
        for row in range(GRID_VERTICAL_COUNT):
            for col in range(GRID_HORIZONTAL_COUNT):
                if self.env.is_food(col, row):
                    food = Food(col * T.block_width() +
                                11, row * T.block_height() + 1)
                    self.foods.append(food)
                    self.elements.append(food)


class Player(BoundedElement, Drawable):
    def __init__(self, env):
        super().__init__()

        pyxel.image(0).load(0, 0, 'ruby.png')
        self.env = env

        block_width = pyxel.width / GRID_HORIZONTAL_COUNT
        block_height = pyxel.height / GRID_VERTICAL_COUNT

        self.height = 20
        self.width = 28
        self.x = 100
        self.y = 200

        self.v_vert = GRAVITY_VELOCITY_START
        self.v_hor = 0.0
        self.dir = DIR_LEFT

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

    def is_hmove_btn(self):
        return pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_A)

    def read_input(self):
        if pyxel.btn(pyxel.KEY_D):
            self.v_hor += VELOCITY_MOVE_STEP
            self.v_hor = min(self.v_hor, VELOCITY_MOVE_MAX)
            self.dir = DIR_RIGHT
            self.env.eventloop.send(EVENT_WALK_START)

        if pyxel.btn(pyxel.KEY_A):
            self.v_hor -= VELOCITY_MOVE_STEP
            self.v_hor = max(self.v_hor, -VELOCITY_MOVE_MAX)
            self.dir = DIR_LEFT
            self.env.eventloop.send(EVENT_WALK_START)

        if self.env.is_at_bottom(self):
            if pyxel.btnp(pyxel.KEY_W):
                self.v_vert = VELOCITY_JUMP

        if pyxel.btnr(pyxel.KEY_W) and self.vmove_up():
            self.v_vert = -DISTANCE_ZERO_THRESHOLD

        if pyxel.btnr(pyxel.KEY_A) or pyxel.btnr(pyxel.KEY_D):
            self.env.eventloop.send(EVENT_WALK_STOP)

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

            if self.env.is_at_bottom(self) and not self.is_hmove_btn():
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
                self.v_vert = -DISTANCE_ZERO_THRESHOLD
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

    def check_food(self):
        self.env.eventloop.send(EVENT_EAT_TRY, self)

    def update(self):
        self.read_input()
        self.update_move()
        self.update_jump()
        self.update_fall()
        self.check_food()

    def draw(self):
        pyxel.blt(self.x, pyxel.height - self.y - self.height, 0, 0, 0, 28, 20)
        # T.rect(self.x, self.y, self.width, self.height, c=15)
        # T.rect(self.x + 5, self.y, 6, 6, c=0)
        if self.dir == DIR_LEFT:
        #     T.rect(self.x, self.y + self.height - 12, 6, 6, c=0)
            pyxel.blt(self.x, pyxel.height - self.y - self.height, 0, 0, 0, -28, 20)
        else:
            pyxel.blt(self.x, pyxel.height - self.y - self.height, 0, 0, 0, 28, 20)
        #     T.rect(self.x + self.width - 6, self.y +
        #            self.height - 12, 6, 6, c=0)


class Score(Drawable):
    def __init__(self, env):
        super().__init__()

        self.score = 0
        env.eventloop.sub(EVENT_EAT_SUCCESS, self.inc)

    def inc(self, _):
        self.score += 1

    def draw(self):
        pyxel.text(pyxel.width - 8, 4, str(self.score), 6)
