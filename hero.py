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
        self.height = 64 * 3
        self.knockback = 20.0
        self.duration = 5 / FRAMES_PER_ACTION
        self.elapsed = 0.0

    def enter(self, e):
        self.hero.frame = 0
        self.elapsed = 0.0
        self.hero.x -= self.knockback * self.hero.vx
        self.hero.y -= self.knockback * self.hero.vy

    def exit(self, e):
        pass

    def do(self):
        ft = game_framework.frame_time
        self.elapsed += ft
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 5

        if self.elapsed >= self.duration:
            self.exit(None)
            moving = (self.hero.vx != 0 or self.hero.vy != 0)
            next_state = self.hero.MOVE if moving else self.hero.IDLE
            next_state.enter(('AUTO', None))
            self.hero.state_machine.cur_state = next_state

    def draw(self, sx, sy):
        cam = game_world.camera
        dw, dh = cam.scale_size(64, 64)
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.hurt_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)


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

        # self.hero.x += self.hero.vx * RUN_SPEED_PPS * ft
        # self.hero.y += self.hero.vy * RUN_SPEED_PPS * ft

        if self.elapsed >= self.duration:
            self.exit(None)
            moving = (self.hero.vx != 0 or self.hero.vy != 0)
            next_state = self.hero.MOVE if moving else self.hero.IDLE
            next_state.enter(('AUTO', None))
            self.hero.state_machine.cur_state = next_state

    def draw(self, sx, sy):
        cam = game_world.camera
        dw, dh = cam.scale_size(64, 64)
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.walk_attack_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)

    def get_attack_bb(self):
        x = self.hero.x
        y = self.hero.y
        if self.hero.face_dir == 1:
            return x, y - 15, x + 24, y + 15
        elif self.hero.face_dir == 2:
            return x - 24, y - 15, x, y + 15
        elif self.hero.face_dir == 3:
            return x - 15, y, x + 15, y + 24
        elif self.hero.face_dir == 4:
            return x - 15, y - 24, x + 15, y

class Move:
    def __init__(self, hero):
        self.hero = hero
        self.height = 64 * 3

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        ft = game_framework.frame_time
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 6
        self.hero.x += self.hero.vx * RUN_SPEED_PPS * ft
        self.hero.y += self.hero.vy * RUN_SPEED_PPS * ft

    def draw(self, sx, sy):
        cam = game_world.camera
        dw, dh = cam.scale_size(64, 64)
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.walk_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)


class Idle:
    def __init__(self, hero):
        self.hero = hero
        self.height = 64 * 3

    def enter(self, e):
        self.hero.vx = 0
        self.hero.vy = 0

    def exit(self, e):
        pass

    def do(self):
        ft = game_framework.frame_time
        self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 4

    def draw(self, sx, sy):
        cam = game_world.camera
        dw, dh = cam.scale_size(64, 64)
        if self.hero.face_dir == 1:
            self.height = 64 * 1
        elif self.hero.face_dir == 2:
            self.height = 64 * 2
        elif self.hero.face_dir == 3:
            self.height = 0
        elif self.hero.face_dir == 4:
            self.height = 64 * 3
        self.hero.idle_image.clip_draw(int(self.hero.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)

class Hero:
    def __init__(self):
        self.x = 50
        self.y = 850
        self.frame = 0
        self.face_dir = 1
        self.vx = 0
        self.vy = 0
        self.keys_pressed = set()
        self.max_hp = 500
        self.hp = 500
        self.level = 1
        self.exp = 0
        self.next_exp = 20
        self.atk = 20
        self.defense = 20

        self.idle_image = load_image('Assets/hero/hero_idle.png')
        self.walk_image = load_image('Assets/hero/hero_walk.png')
        self.walk_attack_image = load_image('Assets/hero/hero_walk_attack.png')
        self.hurt_image = load_image('Assets/hero/hero_hurt.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.ATTACK = Attack(self)
        self.HURT = Hurt(self)

        self.state_machine = StateMachine(self.IDLE, {
            self.IDLE: { right_down: self.MOVE, left_down: self.MOVE, up_down: self.MOVE, down_down: self.MOVE, a_down: self.ATTACK },
            self.MOVE: { right_up: self.IDLE, left_up: self.IDLE, up_up: self.IDLE, down_up: self.IDLE,
                         right_down: self.MOVE, left_down: self.MOVE, up_down: self.MOVE, down_down: self.MOVE,
                         a_down: self.ATTACK },
            self.ATTACK: {},
            self.HURT: {}
        })

    def get_exp(self, amount):
        self.exp += amount
        while self.exp >= self.next_exp:
            self.exp -= self.next_exp
            self.level_up()

    def level_up(self):
        self.level += 1
        self.next_exp = 20 + (self.level^2) * 5
        self.max_hp += 30
        self.atk += 5
        self.defense += 2
        self.hp = self.max_hp

    def get_body_bb(self):
        return self.x - 6, self.y - 13, self.x + 6, self.y - 6

    def get_attack_bb(self):
        if self.state_machine.cur_state is self.ATTACK:
            return self.ATTACK.get_attack_bb()
        return None

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

        self.vx = vx
        self.vy = vy

        ft = game_framework.frame_time
        self.x += self.vx * RUN_SPEED_PPS * ft
        self.y += self.vy * RUN_SPEED_PPS * ft

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

        attack_bb = self.get_attack_bb()
        if attack_bb:
            ax1, ay1, ax2, ay2 = attack_bb
            ax1, ay1 = cam.world_to_screen(ax1, ay1)
            ax2, ay2 = cam.world_to_screen(ax2, ay2)
            draw_rectangle(ax1, ay1, ax2, ay2)

    def get_bb(self):
        return self.get_body_bb()

    def handle_collision(self, group, other):
        if group == 'hero_body:slime' and self.state_machine.cur_state != self.HURT:
            self.state_machine.cur_state.exit(None)
            self.HURT.enter(None)
            self.state_machine.cur_state = self.HURT
            self.hp -= 50
            self.vx, self.vy = 0, 0
        if group == 'hero_body:goblin' and self.state_machine.cur_state != self.HURT:
            self.state_machine.cur_state.exit(None)
            self.HURT.enter(None)
            self.state_machine.cur_state = self.HURT
            self.hp -= 50
            self.vx, self.vy = 0, 0
        if group == 'hero_body:wall':
            wall_left, wall_bottom, wall_right, wall_top = other.get_bb()
            hero_left, hero_bottom, hero_right, hero_top = self.get_bb()

            # 겹친 정도 계산
            overlap_left = hero_right - wall_left
            overlap_right = wall_right - hero_left
            overlap_bottom = hero_top - wall_bottom
            overlap_top = wall_top - hero_bottom

            # 가장 작은 겹침으로 밀어내기
            min_overlap = min(overlap_left, overlap_right, overlap_bottom, overlap_top)

            if min_overlap == overlap_left:
                self.x -= overlap_left
            elif min_overlap == overlap_right:
                self.x += overlap_right
            elif min_overlap == overlap_bottom:
                self.y -= overlap_bottom
            elif min_overlap == overlap_top:
                self.y += overlap_top
        if group == 'hero_attack:slime':
            pass
        if group == 'hero_attack:goblin':
            pass