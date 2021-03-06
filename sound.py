import pyxel
from globals import *

SOUND_EAT = 0
SOUND_WALK = 1
SOUND_BACKGROUND = 2


class SoundEffects:
    def __init__(self, env):
        self.env = env
        self.env.eventloop.sub(EVENT_EAT_SUCCESS, self.eat_effect)
        self.env.eventloop.sub(EVENT_WALK_START, self.walk_effect)
        self.env.eventloop.sub(EVENT_WALK_STOP, self.walk_effect_stop)
        self.env.eventloop.sub(EVENT_GAME_START, self.background_effect)

        pyxel.sound(SOUND_EAT).set('E2E3', 'SS', '77', 'NN', 10)
        pyxel.sound(SOUND_WALK).set('E1C1', 'SS', '66', 'NN', 5)
        pyxel.sound(SOUND_BACKGROUND).set(
            'A0 F0 C0 G0', 'SSSS', '5555', 'FFFF', 100)

    def eat_effect(self, _):
        pyxel.play(1, SOUND_EAT)

    def walk_effect(self, _):
        pyxel.play(2, SOUND_WALK, loop=True)

    def walk_effect_stop(self, _):
        pyxel.stop(2)

    def background_effect(self, _):
        pyxel.play(0, SOUND_BACKGROUND, loop=True)
