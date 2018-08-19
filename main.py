import pyxel

from globals import *
from env import *
from ui import *
from sound import *


class App:
    def __init__(self):
        pyxel.init(256, 256, fps=60, caption="Ruby eats poo", border_width=16, border_color=8, scale=2)

        self.env = Env()
        self.sound = SoundEffects(self.env)
        self.scene = Drawable()
        self.scene.elements.append(Blocks(self.env))
        self.scene.elements.append(Player(self.env))
        self.scene.elements.append(Foods(self.env))
        self.scene.elements.append(Score(self.env))

        self.env.eventloop.send(EVENT_GAME_START)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_ESCAPE):
            exit()

        self.scene.update()

    def draw(self):
        pyxel.cls(7)
        self.scene.draw()


if __name__ == "__main__":
    App()
