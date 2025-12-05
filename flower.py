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

animation_names = ['Idle', 'Attack', 'Death', 'hurt']

def start_pos(box_x=6, box_y=4):
    m = game_world.map
    max_x = m.map_width - 1
    max_y = m.map_height - 1
    hero = game_world.hero

    while True:
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        dist = ((x - hero.x) ** 2 + (y - hero.y) ** 2) ** 0.5

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

        if not lap and dist > 100:
            return x, y

class Flower:
    images = {}
    font = None

    def load_images(self):
        Flower.images['Idle'] = load_image(f'Assets/flower/Flower1_Idle.png')
        Flower.images['Attack'] = load_image(f'Assets/flower/Flower1_Attack.png')
        Flower.images['Death'] = load_image(f'Assets/flower/Flower1_Death.png')
        Flower.images['Hurt'] = load_image(f'Assets/flower/Flower1_Hurt.png')
        if Flower.font is None:
            Flower.font = load_font('Assets/DNFBitBitv2.otf', 16)

    def __init__(self):
        self.x, self.y = start_pos()
        self.prev_x = self.x
        self.prev_y = self.y
        self.face_dir = random.randint(1, 4) # 앞뒤좌우
        self.load_images()
        self.frame = random.randint(0, 4)
        self.vx = 1
        self.vy = 1
        self.wait_time = get_time()
        self.height = 64 * 3
        self.hp = 110
        self.atk = 30
        self.defense = 0
        self.flower_state = 'Idle'
        self.frame_num = 4
        self.damage_cool = 0

    def near_by_hero(self):
        hero = game_world.hero
        distance = ((self.x - hero.x) ** 2 + (self.y - hero.y) ** 2) ** 0.5
        if distance < 40:
            return 'attack'
        if distance < 100:
            return 'near'
        else:
            return 'none'

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_num

        if self.damage_cool > 0:
            self.damage_cool -= game_framework.frame_time

        if self.flower_state == 'Idle' and get_time() - self.wait_time > 2:
            self.wait_time = get_time()
            self.face_dir = random.randint(1, 4)

        if self.flower_state == 'Attack' and int(self.frame) >= 6:
            self.flower_state = 'Idle'
            self.frame = 0
            self.frame_num = 4
            self.vx = 1
            self.vy = 1

        if self.flower_state == 'Hurt' and get_time() - self.wait_time > 0.5:
            self.flower_state = 'Idle'
            self.vx = 1
            self.vy = 1

        if self.flower_state == 'Death':
            if int(self.frame) >= 9:
                game_world.hero.get_exp(6)
                game_world.hero.get_gold(5)
                game_world.remove_object(self)

                new = Flower()
                new.x, new.y = start_pos()
                game_world.add_object(new, 1)

                game_world.add_collision_pair('hero_body:flower', None, new)
                game_world.add_collision_pair('hero_attack:flower', None, new)
                print("식인꽃 리스폰")
            return

        elif self.near_by_hero() == 'attack' and self.flower_state != 'Attack' and self.flower_state != 'Hurt':
            self.flower_state = 'Attack'
            self.frame_num = 7
            self.frame = 0
            self.vx = 0
            self.vy = 0

        hero = game_world.hero
        dx = hero.x - self.x
        dy = hero.y - self.y

        if abs(dx) > abs(dy):
            self.face_dir = 4 if dx > 0 else 3
        else:
            self.face_dir = 2 if dy > 0 else 1

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
        Flower.images[self.flower_state].clip_draw(int(self.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)

        hp_text = f"{self.hp}/110"
        Flower.font.draw(sx - 33, sy + 30, hp_text, (255, 255, 255))

        hx1, hy1, hx2, hy2 = self.get_bb()
        hx1, hy1 = cam.world_to_screen(hx1, hy1)
        hx2, hy2 = cam.world_to_screen(hx2, hy2)
        draw_rectangle(hx1, hy1, hx2, hy2)

    def get_bb(self):
        if self.flower_state == 'Attack':
            if self.face_dir == 1:
                return self.x - 13, self.y - 15, self.x + 13, self.y + 10
            elif self.face_dir == 2:
                return self.x - 13, self.y - 10, self.x + 13, self.y + 16
            elif self.face_dir == 3:
                return self.x - 19, self.y - 10, self.x + 17, self.y + 14
            elif self.face_dir == 4:
                return self.x - 17, self.y - 10, self.x + 19, self.y + 14
        return self.x - 6, self.y - 12, self.x + 6, self.y - 5

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'hero_attack:flower':
            if self.flower_state == 'Hurt' or self.flower_state == 'Death':
                return
            if self.damage_cool > 0:
                return
            print("flower hit by hero")
            self.hp = self.hp - other.atk + self.defense
            self.damage_cool = 0.2
            if self.hp <= 0:
                self.flower_state = 'Death'
                self.frame = 0
                self.frame_num = 10
            else:
                self.flower_state = 'Hurt'
                self.frame = 0
                self.frame_num = 5
                self.wait_time = get_time()
        if group == 'hero_body:flower':
            pass