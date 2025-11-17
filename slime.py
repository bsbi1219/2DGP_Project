from pico2d import *
import game_framework
import game_world
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

animation_names = ['Walk', 'Run', 'Attack', 'Death']

class Slime:
    images = {}

    def load_images(self):
        Slime.images['Walk'] = load_image(f'Assets/slime/slime 1/Slime1_Walk.png')
        Slime.images['Run'] = load_image(f'Assets/slime/slime 1/Slime1_Run.png')
        Slime.images['Attack'] = load_image(f'Assets/slime/slime 1/Slime1_Attack.png')
        Slime.images['Death'] = load_image(f'Assets/slime/slime 1/Slime1_Death.png')

    def __init__(self):
        self.x, self.y = random.randint(100, 1000), random.randint(100, 900)
        self.load_images()
        self.frame = random.randint(0, 9)
        self.vx = random.choice([-1, 1])
        self.vy = random.choice([-1, 1])
        self.wait_time = get_time()
        self.height = 64 * 3
        self.hp = 150
        self.atk = 20
        self.defense = 0
        self.slime_state = 'WALK'

    def get_bb(self):
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if get_time() - self.wait_time > 2:
            self.wait_time = get_time()
            self.vx = random.choice([-1, 0, 1])
            self.vy = random.choice([-1, 0, 1])
        pass

    def draw(self):
        if self.vx < 0:
            pass
        else:
            pass

    def handle_event(self, event):
        pass

    def handle_collision(self, other, group):
        pass