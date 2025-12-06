from pico2d import *
import game_framework
import game_world
import random

PIXEL_PER_METER = (10.0 / 1.2)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Idle', 'Walk', 'Run', 'Attack', 'Death', 'hurt']

class Boss:
    images = {}

    def load_images(self):
        Boss.images['Idle'] = load_image(f'Assets/Boss/boss_Idle.png')
        Boss.images['Walk'] = load_image("Assets/Boss/boss_Walk.png")
        Boss.images['Run'] = load_image("Assets/Boss/boss_Run.png")
        Boss.images['Attack'] = load_image("Assets/Boss/boss_Attack.png")
        Boss.images['Death'] = load_image("Assets/Boss/boss_Death.png")
        Boss.images['Hurt'] = load_image("Assets/Boss/boss_Hurt.png")

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.prev_x = self.x
        self.prev_y = self.y
        self.face_dir = 1
        self.load_images()
        self.frame = random.randint(0, 4)
        self.vx = 1
        self.vy = 1
        self.wait_time = get_time()
        self.height = 64 * 3
        self.hp = 2000
        self.atk = 20
        self.defense = 0
        self.boss_state = 'Idle'
        self.frame_num = 4
        self.damage_cool = 0

    def get_bb(self):
        left = self.x - 50
        bottom = self.y - 50
        right = self.x + 50
        top = self.y + 50
        return left, bottom, right, top

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        game_world.remove_object(self)
        # 추가적인 보스 사망 처리 로직 (예: 아이템 드랍, 게임 승리 등)

    def update(self):
        # 보스의 행동 로직 구현 (예: 공격 패턴, 이동 등)
        pass

    def draw(self):
        cam = game_world.camera
        sx, sy = cam.world_to_screen(self.x, self.y)
        dw, dh = cam.scale_size(60, 60)

        if self.face_dir == 1:
            self.height = 64 * 3
        elif self.face_dir == 2:
            self.height = 64 * 2
        elif self.face_dir == 3:
            self.height = 64
        elif self.face_dir == 4:
            self.height = 0
        Boss.images[self.boss_state].clip_draw(int(self.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)

        hx1, hy1, hx2, hy2 = self.get_bb()
        hx1, hy1 = cam.world_to_screen(hx1, hy1)
        hx2, hy2 = cam.world_to_screen(hx2, hy2)
        draw_rectangle(hx1, hy1, hx2, hy2)