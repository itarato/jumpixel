import pyxel

from globals import *
from env import *
from ui import *


class App:
    def __init__(self):
        pyxel.init(256, 256, fps=24)

        self.env = Env()
        self.scene = Drawable()
        self.scene.elements.append(Blocks(self.env))
        self.scene.elements.append(Player(self.env))

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_ESCAPE):
            exit()

        self.scene.update()

    def draw(self):
        pyxel.cls(0)
        self.scene.draw()


if __name__ == "__main__":
    App()
