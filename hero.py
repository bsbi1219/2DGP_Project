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

TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Move:
    def __init__(self, hero):
        self.hero = hero
        self.height = 64 * 3

    def enter(self, e):
        if right_down(e):
            self.hero.vx = 1
            self.hero.vy = 0
            self.hero.face_dir = 1
        elif left_down(e):
            self.hero.vx = -1
            self.hero.vy = 0
            self.hero.face_dir = 2
        elif up_down(e):
            self.hero.vx = 0
            self.hero.vy = 1
            self.hero.face_dir = 3
        elif down_down(e):
            self.hero.vx = 0
            self.hero.vy = -1
            self.hero.face_dir = 4

    def exit(self, e):
        pass

    def do(self):
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.hero.x += self.hero.vx * RUN_SPEED_PPS * game_framework.frame_time
        self.hero.y += self.hero.vy * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        self.hero.image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, self.hero.x, self.hero.y, 200, 200)

class Idle:
    def __init__(self, hero):
        self.hero = hero
        self.height = 64 * 3

    def enter(self, e):
        self.hero.wait_time = get_time()
        self.hero.vx = 0
        self.hero.vy = 0

    def exit(self, e):
            pass

    def do(self):
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        self.hero.image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, self.hero.x, self.hero.y, 200, 200)


class Hero:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.face_dir = 1
        self.vx = 0
        self.vy = 0
        self.image = load_image('Assets/hero/hero_idle.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)

        self.state_machine = StateMachine(self.IDLE,{
            self.IDLE: { right_down: self.MOVE, left_down: self.MOVE, up_down: self.MOVE, down_down: self.MOVE },
            self.MOVE: { right_up: self.IDLE, left_up: self.IDLE, up_up: self.IDLE, down_up: self.IDLE }
        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def draw(self):
        self.state_machine.draw()

    def handle_collision(self, group, other):
        pass