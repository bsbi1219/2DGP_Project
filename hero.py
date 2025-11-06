from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN
import game_world
import game_framework
from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    def __init__(self, hero):
        self.hero = hero

    def enter(self, e):
        self.hero.wait_time = get_time()
        self.hero.dir = 0

    def exit(self, e):
            pass

    def do(self):
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        if self.hero.face_dir == 1: # right
            self.hero.image.clip_draw(int(self.hero.frame) * 64, 300, 64, 64, self.hero.x, self.hero.y)
        elif self.hero.face_dir == 2: # left
            self.hero.image.clip_draw(int(self.hero.frame) * 64, 200, 64, 64, self.hero.x, self.hero.y)
        elif self.hero.face_dir == 3: # up
            self.hero.image.clip_draw(int(self.hero.frame) * 64, 200, 64, 64, self.hero.x, self.hero.y)
        elif self.hero.face_dir == 4: # down
            self.hero.image.clip_draw(int(self.hero.frame) * 64, 200, 64, 64, self.hero.x, self.hero.y)


class Hero:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.face_dir = 1
        self.image = load_image('Assets/hero/hero_idle.png')
        self.IDLE = Idle(self)

        self.state_machine = StateMachine(self.IDLE,{ })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()