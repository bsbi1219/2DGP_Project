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

animation_names = ['Walk', 'Run', 'Attack', 'Death']\

class Slime:
    images = {}

    def load_images(self):
        Slime.images['Walk'] = load_image(f'Assets/slime/slime 1/Slime1_Walk.png')
        Slime.images['Run'] = load_image(f'Assets/slime/slime 1/Slime1_Run.png')
        Slime.images['Attack'] = load_image(f'Assets/slime/slime 1/Slime1_Attack.png')
        Slime.images['Death'] = load_image(f'Assets/slime/slime 1/Slime1_Death.png')

    def __init__(self):
        self.x, self.y = random.randint(100, 1000), random.randint(100, 900)
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

    def get_bb(self):
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if self.slime_state == 'Walk' and get_time() - self.wait_time > 2:
            self.wait_time = get_time()
            self.face_dir = random.randint(1, 4)
        if self.face_dir == 1:
            self.y -= self.vy * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 2:
            self.y += self.vy * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 3:
            self.x -= self.vx * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 4:
            self.x += self.vx * RUN_SPEED_PPS * game_framework.frame_time
        pass

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

    def handle_collision(self, other, group):
        if group == 'slime:wall':
            if self.face_dir == 1:
                self.face_dir = 2
            elif self.face_dir == 2:
                self.face_dir = 1
            elif self.face_dir == 3:
                self.face_dir = 4
            elif self.face_dir == 4:
                self.face_dir = 3