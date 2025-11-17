from pico2d import *
import game_framework
from state_machine import StateMachine
import random

PIXEL_PER_METER = (10.0 / 1.0)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

class Slime:
    images = None

    def load_images(self):
        pass

    def __init__(self):
        self.x, self.y = random.randint(100, 1000), random.randint(100, 900)
        self.load_images()
        self.frame = random.randint(0, 9)
        self.vx = random.choice([-1, 1])
        self.vy = random.choice([-1, 1])

    def get_bb(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, other, group):
        pass