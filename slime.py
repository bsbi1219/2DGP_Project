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
        Slime.images['hurt'] = load_image(f'Assets/slime/slime 1/Slime1_Hurt.png')

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

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if self.slime_state == 'Walk' and get_time() - self.wait_time > 2:
            self.wait_time = get_time()
            self.face_dir = random.randint(1, 4)
        if self.slime_state == 'Hurt' and get_time() - self.wait_time > 0.5:
            self.slime_state = 'Walk'
        if self.slime_state == 'Death':
            pass
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
            attack_bb = other.get_attack_bb()
            if attack_bb is None:
                return

            ax1, ay1, ax2, ay2 = attack_bb
            bx1, by1, bx2, by2 = self.get_bb()

            if not (ax1 > bx2 or ax2 < bx1 or ay2 < by1 or ay1 > by2):
                print("slime hit by hero")

                self.hp -= other.atk - self.defense

                if self.hp <= 0:
                    self.slime_state = 'Death'
                else:
                    self.slime_state = 'hurt'
                    self.wait_time = get_time()