from pico2d import *
import game_framework
from state_machine import StateMachine
import game_world

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


PIXEL_PER_METER = (10.0 / 1.2)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Hurt:
    def __init__(self, hero):
        self.hero = hero

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self, sx, sy):
        pass

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

    def draw(self, sx, sy):
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.walk_attack_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, sx, sy, 300, 300)

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

    def draw(self, sx, sy):
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.walk_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, sx, sy, 300, 300)

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

    def draw(self, sx, sy):
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.idle_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, sx, sy, 300, 300)

class Hero:
    def __init__(self):
        self.x = 50
        self.y = 850
        self.frame = 0
        self.face_dir = 1
        self.vx = 0
        self.vy = 0
        self.keys_pressed = set()
        self.hp = 500
        self.level = 1
        self.exp = 0
        self.atk = 20
        self.defense = 20

        self.idle_image = load_image('Assets/hero/hero_idle.png')
        self.walk_image = load_image('Assets/hero/hero_walk.png')
        self.walk_attack_image = load_image('Assets/hero/hero_walk_attack.png')
        self.hurt_image = load_image('Assets/hero/hero_hurt.png')

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

        length = (vx ** 2 + vy ** 2) ** 0.5
        if length != 0:
            vx /= length
            vy /= length

        ft = game_framework.frame_time
        new_x = self.x + vx * RUN_SPEED_PPS * ft
        new_y = self.y + vy * RUN_SPEED_PPS * ft

        for rect in game_world.map.collision_rects:
            left, bottom, right, top = rect
            hx1 = new_x - 4
            hy1 = new_y - 10
            hx2 = new_x + 4
            hy2 = new_y - 6
            if not (hx2 < left or hx1 > right or hy2 < bottom or hy1 > top):
                # 충돌 감지 -> 간단 처리(기존 처리 유지하거나 축별 분리 권장)
                if vx > 0:
                    new_x = left - 150
                elif vx < 0:
                    new_x = right + 150
                if vy > 0:
                    new_y = bottom - 150
                elif vy < 0:
                    new_y = top + 150

        self.x = new_x
        self.y = new_y
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
        cam = game_world.camera
        sx, sy = cam.world_to_screen(self.x, self.y)
        cur = self.state_machine.cur_state
        cur.draw(sx, sy)
        hx1, hy1, hx2, hy2 = self.get_bb()
        hx1, hy1 = cam.world_to_screen(hx1, hy1)
        hx2, hy2 = cam.world_to_screen(hx2, hy2)
        draw_rectangle(hx1, hy1, hx2, hy2)

    def get_bb(self):
        return self.x - 4, self.y - 10, self.x + 4, self.y - 6

    def handle_collision(self, group, other):
        pass
