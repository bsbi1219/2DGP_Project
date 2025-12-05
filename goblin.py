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

def start_pos(box_x=8):
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
        bottom = y - 8
        top = y + 5

        lap = False
        for rect in m.collision_rects:
            rl, rb, rr, rt = rect
            if not (right < rl or left > rr or top < rb or bottom > rt):
                lap = True
                break

        if not lap and dist > 100:
            return x, y

class Goblin:
    images = {}
    font = None

    def load_images(self):
        Goblin.images['Walk'] = load_image(f'Assets/goblin/goblin 1/orc1_walk.png')
        Goblin.images['Run'] = load_image(f'Assets/goblin/goblin 1/orc1_run.png')
        Goblin.images['Attack'] = load_image(f'Assets/goblin/goblin 1/orc1_attack.png')
        Goblin.images['Death'] = load_image(f'Assets/goblin/goblin 1/orc1_death.png')
        Goblin.images['Hurt'] = load_image(f'Assets/goblin/goblin 1/orc1_hurt.png')
        if Goblin.font is None:
            Goblin.font = load_font('Assets/DNFBitBitv2.otf', 16)

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
        self.hp = 200
        self.atk = 15
        self.defense = 0
        self.goblin_state = 'Walk'
        self.frame_num = 6
        self.damage_cool = 0

    def near_by_hero(self):
        hero = game_world.hero
        distance = ((self.x - hero.x) ** 2 + (self.y - hero.y) ** 2) ** 0.5
        if distance < 28:
            return 'attack'
        elif distance < 100:
            return 'run'
        else:
            return 'none'

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_num

        if self.damage_cool > 0:
            self.damage_cool -= game_framework.frame_time

        if self.goblin_state == 'Walk' and get_time() - self.wait_time > 2:
            self.wait_time = get_time()
            self.face_dir = random.randint(1, 4)

        if self.goblin_state == 'Attack' and int(self.frame) >= 7:
            self.goblin_state = 'Walk'
            self.frame = 0
            self.frame_num = 6
            self.vx = 1
            self.vy = 1

        if self.goblin_state == 'Hurt' and get_time() - self.wait_time > 0.5:
            self.goblin_state = 'Walk'
            self.frame = 0
            self.frame_num = 6
            self.vx = 1
            self.vy = 1

        if self.goblin_state == 'Death':
            if int(self.frame) >= 7:
                game_world.hero.get_exp(8)
                game_world.hero.get_gold(10)
                game_world.remove_object(self)

                new = Goblin()
                new.x, new.y = start_pos()
                game_world.add_object(new, 1)

                game_world.add_collision_pair('hero_body:goblin', None, new)
                game_world.add_collision_pair('hero_attack:goblin', None, new)
                game_world.add_collision_pair('slime:wall', new, None)
                print("고블린 리스폰")
            return

        if self.near_by_hero() == 'run' and self.goblin_state != 'Run' and self.goblin_state != 'Attack' and self.goblin_state != 'Hurt':
            self.goblin_state = 'Run'
            self.frame_num = 8
            self.vx = 1
            self.vy = 1
        elif self.near_by_hero() == 'attack' and self.goblin_state != 'Attack' and self.goblin_state != 'Hurt':
            self.goblin_state = 'Attack'
            self.frame_num = 8
            self.frame = 0
            self.vx = 0
            self.vy = 0

        if self.goblin_state == 'Run':
            if self.near_by_hero() == 'none':
                self.goblin_state = 'Walk'
                self.frame_num = 6
            hero = game_world.hero
            dx = hero.x - self.x
            dy = hero.y - self.y

            if abs(dx) > abs(dy):
                self.face_dir = 4 if dx > 0 else 3
            else:
                self.face_dir = 2 if dy > 0 else 1

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
        Goblin.images[self.goblin_state].clip_draw(int(self.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)

        hp_text = f"{self.hp}/200"
        Goblin.font.draw(sx - 33, sy + 30, hp_text, (255, 255, 255))

        hx1, hy1, hx2, hy2 = self.get_bb()
        hx1, hy1 = cam.world_to_screen(hx1, hy1)
        hx2, hy2 = cam.world_to_screen(hx2, hy2)
        draw_rectangle(hx1, hy1, hx2, hy2)

    def get_bb(self):
        if self.goblin_state == 'Attack':
            if self.face_dir == 1:
                return self.x - 19, self.y - 18, self.x + 19, self.y + 5
            if self.face_dir == 2:
                return self.x - 19, self.y - 5, self.x + 19, self.y + 18
            if self.face_dir == 3:
                return self.x - 23, self.y - 15, self.x + 5, self.y + 13
            if self.face_dir == 4:
                return self.x - 5, self.y - 15, self.x + 23, self.y + 13
        return self.x - 8, self.y - 8, self.x + 8, self.y + 5

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'goblin:wall':
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
        if group == 'hero_attack:goblin':
            if self.goblin_state == 'Hurt' or self.goblin_state == 'Death':
                return
            if self.damage_cool > 0:
                return
            self.hp -= other.atk - self.defense
            self.damage_cool = 0.2
            if self.hp <= 0:
                self.goblin_state = 'Death'
                self.frame = 0
                self.frame_num = 8
            else:
                self.goblin_state = 'Hurt'
                self.frame = 0
                self.frame_num = 6
                self.wait_time = get_time()
        if group == 'hero_body:goblin':
            pass