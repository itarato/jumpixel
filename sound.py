import pyxel
from globals import *

SOUND_EAT = 0
SOUND_WALK = 1


class SoundEffects:
    def __init__(self, env):
        self.env = env
        self.env.eventloop.sub(EVENT_EAT_SUCCESS, self.eat_effect)
        self.env.eventloop.sub(EVENT_WALK_START, self.walk_effect)
        self.env.eventloop.sub(EVENT_WALK_STOP, self.walk_effect_stop)

        pyxel.sound(SOUND_EAT).set('E2E3', 'PP', '77', 'NN', 10)
        pyxel.sound(SOUND_WALK).set('E1C1', 'NN', '66', 'NN', 5)

    def eat_effect(self, _):
        pyxel.play(1, 0)

    def walk_effect(self, _):
        pyxel.play(1, 1, loop=True)

    def walk_effect_stop(self, _):
        pyxel.stop(1)
