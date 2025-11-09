from pico2d import *
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

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Attack:
    def __init__(self, hero):
        self.hero = hero
        self.height = 64 * 3
        self.duration = 0.5
        self.elapsed = 0.0

    def enter(self, e):
        self.hero.frame = 0
        self.elapsed = 0.0

    def exit(self, e):
        pass

    def do(self):
        ft = game_framework.frame_time
        self.elapsed += ft
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 6

        self.hero.x += self.hero.vx * RUN_SPEED_PPS * ft
        self.hero.y += self.hero.vy * RUN_SPEED_PPS * ft

        if self.elapsed >= self.duration:
            self.exit(None)
            moving = (self.hero.vx != 0 or self.hero.vy != 0)
            next_state = self.hero.MOVE if moving else self.hero.IDLE
            next_state.enter(('AUTO', None))
            self.hero.state_machine.cur_state = next_state

    def draw(self):
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.walk_attack_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, self.hero.x, self.hero.y, 32, 32)

class Move:
    def __init__(self, hero):
        self.hero = hero
        self.height = 64 * 3

    def enter(self, e):
        # 키 홀드 방식이면 속도는 Hero.update에서 결정하므로 별도 처리 없음
        pass

    def exit(self, e):
        pass

    def do(self):
        ft = game_framework.frame_time
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 6
        self.hero.x += self.hero.vx * RUN_SPEED_PPS * ft
        self.hero.y += self.hero.vy * RUN_SPEED_PPS * ft

    def draw(self):
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.walk_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, self.hero.x, self.hero.y, 32, 32)

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
        ft = game_framework.frame_time
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 4

    def draw(self):
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.idle_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, self.hero.x, self.hero.y, 32, 32)

class Hero:
    def __init__(self):
        self.x = 50
        self.y = 850
        self.frame = 0
        self.face_dir = 1
        self.vx = 0
        self.vy = 0
        self.keys_pressed = set()

        self.idle_image = load_image('Assets/hero/hero_idle.png')
        self.walk_image = load_image('Assets/hero/hero_walk.png')
        self.walk_attack_image = load_image('Assets/hero/hero_walk_attack.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.ATTACK = Attack(self)

        self.state_machine = StateMachine(self.IDLE, {
            self.IDLE: { right_down: self.MOVE, left_down: self.MOVE, up_down: self.MOVE, down_down: self.MOVE, a_down: self.ATTACK },
            self.MOVE: { right_up: self.IDLE, left_up: self.IDLE, up_up: self.IDLE, down_up: self.IDLE,
                         right_down: self.MOVE, left_down: self.MOVE, up_down: self.MOVE, down_down: self.MOVE,
                         a_down: self.ATTACK },
            self.ATTACK: {}
        })

    def update(self):
        vx = 0
        vy = 0
        if SDLK_RIGHT in self.keys_pressed:
            vx += 1
        if SDLK_LEFT in self.keys_pressed:
            vx -= 1
        if SDLK_UP in self.keys_pressed:
            vy += 1
        if SDLK_DOWN in self.keys_pressed:
            vy -= 1

        self.vx = vx
        self.vy = vy

        if self.vx > 0:
            self.face_dir = 1
        elif self.vx < 0:
            self.face_dir = 2
        elif self.vy > 0:
            self.face_dir = 3
        elif self.vy < 0:
            self.face_dir = 4

        cur = self.state_machine.cur_state
        moving = (self.vx != 0 or self.vy != 0)
        if moving and cur is self.IDLE:
            cur.exit(None)
            self.MOVE.enter(('HOLD', None))
            self.state_machine.cur_state = self.MOVE
        elif (not moving) and cur is self.MOVE:
            cur.exit(None)
            self.IDLE.enter(('HOLD', None))
            self.state_machine.cur_state = self.IDLE

        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            self.keys_pressed.add(event.key)
        elif event.type == SDL_KEYUP:
            self.keys_pressed.discard(event.key)

        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 6, self.y - 8, self.x + 6, self.y + 8

    def handle_collision(self, group, other):
        pass
