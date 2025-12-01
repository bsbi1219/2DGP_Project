from pico2d import *
import game_framework
import game_world
from state_machine import StateMachine
import random

PIXEL_PER_METER = (10.0 / 1.2)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Run', 'Attack', 'Death', 'hurt']

def start_pos(box_x=6, box_y=4):
    m = game_world.map
    max_x = m.map_width - 1
    max_y = m.map_height - 1

    # 충돌박스와 겹치지 않는 위치 찾기
    while True:
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        left = x - box_x
        right = x + box_x
        bottom = y - box_y
        top = y + box_y

        lap = False
        for rect in m.collision_rects:
            rl, rb, rr, rt = rect
            if not (right < rl or left > rr or top < rb or bottom > rt):
                lap = True
                break

        if not lap:
            return x, y

class Slime:
    images = {}

    def load_images(self):
        Slime.images['Walk'] = load_image(f'Assets/slime/slime 1/Slime1_Walk.png')
        Slime.images['Run'] = load_image(f'Assets/slime/slime 1/Slime1_Run.png')
        Slime.images['Attack'] = load_image(f'Assets/slime/slime 1/Slime1_Attack.png')
        Slime.images['Death'] = load_image(f'Assets/slime/slime 1/Slime1_Death.png')
        Slime.images['Hurt'] = load_image(f'Assets/slime/slime 1/Slime1_Hurt.png')

    def __init__(self):
        self.x, self.y = start_pos()
        self.prev_x = self.x
        self.prev_y = self.y
        self.face_dir = 1 # 앞뒤좌우
        self.load_images()
        self.frame = random.randint(0, 7)
        self.vx = 1
        self.vy = 1
        self.wait_time = get_time()
        self.height = 64 * 3
        self.hp = 150
        self.atk = 20
        self.defense = 0
        self.slime_state = 'Walk'
        self.frame_num = 8

    def near_by_hero(self):
        hero = game_world.hero
        distance = ((self.x - hero.x) ** 2 + (self.y - hero.y) ** 2) ** 0.5
        if distance < 20:
            return 'attack'
        elif distance < 100:
            return 'run'

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_num

        if self.slime_state == 'Walk' and get_time() - self.wait_time > 2:
            self.wait_time = get_time()
            self.face_dir = random.randint(1, 4)

        if self.slime_state == 'Attack' and int(self.frame) >= 7:
            self.slime_state = 'Walk'
            self.frame = 0
            self.frame_num = 8
            self.vx = 1
            self.vy = 1

        if self.slime_state == 'Hurt' and get_time() - self.wait_time > 0.5:
            self.slime_state = 'Walk'

        if self.slime_state == 'Death':
            if int(self.frame) >= 9:
                game_world.hero.get_exp(6)
                game_world.hero.get_gold(5)
                game_world.remove_object(self)
            return

        if self.slime_state == 'Run':
            hero = game_world.hero
            dx = hero.x - self.x
            dy = hero.y - self.y

            if abs(dx) > abs(dy):
                self.face_dir = 4 if dx > 0 else 3
            else:
                self.face_dir = 2 if dy > 0 else 1

        if self.near_by_hero() == 'run' and self.slime_state != 'Run' and self.slime_state != 'Attack':
            self.slime_state = 'Run'
            self.frame_num = 8
        elif self.near_by_hero() == 'attack' and self.slime_state != 'Attack':
            self.slime_state = 'Attack'
            self.frame_num = 8
            self.frame = 0
            self.vx = 0
            self.vy = 0

        if self.face_dir == 1:
            self.y -= self.vy * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 2:
            self.y += self.vy * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 3:
            self.x -= self.vx * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 4:
            self.x += self.vx * RUN_SPEED_PPS * game_framework.frame_time


    def draw(self):
        cam = game_world.camera
        sx, sy = cam.world_to_screen(self.x, self.y)
        dw, dh = cam.scale_size(48, 48)
        if self.face_dir == 1:
            self.height = 64 * 3
        elif self.face_dir == 2:
            self.height = 64 * 2
        elif self.face_dir == 3:
            self.height = 64
        elif self.face_dir == 4:
            self.height = 0
        Slime.images[self.slime_state].clip_draw(int(self.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)

        hx1, hy1, hx2, hy2 = self.get_bb()
        hx1, hy1 = cam.world_to_screen(hx1, hy1)
        hx2, hy2 = cam.world_to_screen(hx2, hy2)
        draw_rectangle(hx1, hy1, hx2, hy2)

    def get_bb(self):
        if self.slime_state == 'Attack':
            return self.x - 17, self.y - 6, self.x + 17, self.y + 15
        return self.x - 6, self.y - 4, self.x + 6, self.y + 4

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'slime:wall':
            print("slime hit wall")
            self.x = self.prev_x
            self.y = self.prev_y
            if self.face_dir == 1:
                self.face_dir = random.randint(2, 4)
            elif self.face_dir == 2:
                self.face_dir = random.randint(3, 4)
            elif self.face_dir == 3:
                self.face_dir = random.randint(1, 2)
            elif self.face_dir == 4:
                self.face_dir = random.randint(1, 3)
        if group == 'hero_attack:slime':
            if self.slime_state == 'Hurt':
                return
            print("slime hit by hero")
            self.hp = self.hp - other.atk + self.defense
            if self.hp <= 0:
                self.slime_state = 'Death'
                self.frame = 0
                self.frame_num = 10
            else:
                self.slime_state = 'Hurt'
                self.x -= self.vx * 3
                self.y -= self.vy * 3
                self.frame = 0
                self.frame_num = 5
                self.wait_time = get_time()
        if group == 'hero_body:slime':
            pass