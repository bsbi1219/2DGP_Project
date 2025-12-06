from pico2d import *
import game_framework
import game_world
import random
import dialogue_state
from goblin import Goblin

PIXEL_PER_METER = (10.0 / 1.2)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Idle', 'Run', 'Attack', 'Death', 'Hurt', 'Skill', 'Text']

class Boss:
    images = {}

    def load_images(self):
        Boss.images['Idle'] = load_image("Assets/Boss/boss_Idle.png")
        Boss.images['Run'] = load_image("Assets/Boss/boss_Run.png")
        Boss.images['Attack'] = load_image("Assets/Boss/boss_Attack.png")
        Boss.images['Death'] = load_image("Assets/Boss/boss_Death.png")
        Boss.images['BeforeDeath'] = load_image("Assets/Boss/boss_Idle.png")
        Boss.images['Hurt'] = load_image("Assets/Boss/boss_Hurt.png")
        Boss.images['Skill'] = load_image(f'Assets/Boss/boss_Idle.png')
        Boss.images['Text'] = load_image(f'Assets/Boss/boss_Idle.png')

    def __init__(self):
        self.x, self.y = 640, 540
        self.prev_x = self.x
        self.prev_y = self.y
        self.face_dir = 1

        self.load_images()

        self.frame = random.randint(0, 4)
        self.vx = 1
        self.vy = 1
        self.wait_time = get_time()
        self.height = 64 * 3
        self.max_hp = 2000
        self.hp = 2000
        self.atk = 70
        self.defense = 30
        self.boss_state = 'Idle'
        self.frame_num = 4
        self.damage_cool = 0

        self.battle_started = False

        # 고블린 소환
        self.summon_cool = 1000
        self.summon_started = False

        # 대사 관련
        self.used_half_hp_text = False
        self.used_intro_text = False

        self.death_dialogue_done = False

    def start_battle(self):
        self.battle_started = True

    def get_bb(self):
        if self.boss_state == 'Attack' and int(self.frame) >= 8:
            if self.face_dir == 1:
                left = self.x - 20
                bottom = self.y - 45
                right = self.x + 20
                top = self.y
            elif self.face_dir == 2:
                left = self.x - 20
                bottom = self.y - 20
                right = self.x + 20
                top = self.y + 25
            elif self.face_dir == 3:
                left = self.x - 35
                bottom = self.y - 20
                right = self.x + 25
                top = self.y
            elif self.face_dir == 4:
                left = self.x - 25
                bottom = self.y - 20
                right = self.x + 35
                top = self.y
        else:
            if self.face_dir == 1 or self.face_dir == 2:
                left = self.x - 20
                bottom = self.y - 20
                right = self.x + 20
                top = self.y
            elif self.face_dir == 3:
                left = self.x - 15
                bottom = self.y - 20
                right = self.x + 25
                top = self.y
            elif self.face_dir == 4:
                left = self.x - 25
                bottom = self.y - 20
                right = self.x + 15
                top = self.y
        return left, bottom, right, top

    def near_by_hero(self):
        hero = game_world.hero
        distance = ((self.x - hero.x) ** 2 + (self.y - hero.y) ** 2) ** 0.5
        if distance < 30:
            return 'Attack'
        else:
            return 'Run'

    def go_to_clear(self):
        import game_clear_state
        game_framework.change_mode(game_clear_state)

    def update(self):
        hero = game_world.hero
        dt = game_framework.frame_time
        self.summon_cool -= dt

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_num

        if not self.used_intro_text and hero.y > 480:
            self.used_intro_text = True
            dialogue_state.set_message("...인간 따위가 감히 내 앞에 서다니.")
            dialogue_state.set_message("죽고 싶어서 온건가?")
            dialogue_state.set_message("그렇다면 죽여주마...")
            game_framework.push_mode(dialogue_state)
            hero.vx = 0
            hero.vy = 0
            game_world.hero.state_machine.cur_state = game_world.hero.IDLE

            dialogue_state.on_close = self.start_battle
            return

        if not self.battle_started:
            return

        if self.hp < 1000 and not self.used_half_hp_text:
            self.used_half_hp_text = True
            self.boss_state = "Text"
            dialogue_state.set_message("인간 치고는 제법이군. 하지만 지금부터는 봐주지 않겠다.")
            game_framework.push_mode(dialogue_state)
            dialogue_state.on_close = self.resume_after_text
            self.summon_started = True
            self.summon_cool = 15
            return

        if self.boss_state == 'Death':
            # 죽는 애니메이션 프레임 진행
            self.frame += FRAMES_PER_ACTION * dt

            # death 스프라이트가 11프레임(0~10)이니까 그 이상 되면 클리어 화면으로
            if self.frame >= 11:
                import game_clear_state
                game_framework.change_mode(game_clear_state)
            return

        if self.near_by_hero() == 'Attack' and self.boss_state != 'Attack' and self.boss_state != 'Hurt':
            self.boss_state = 'Attack'
            self.frame_num = 12
            self.frame = 0
            self.vx = 0
            self.vy = 0
            return

        if self.near_by_hero() == 'Run' and self.boss_state != 'Run' and self.boss_state != 'Attack' and self.boss_state != 'Hurt':
            self.boss_state = 'Run'
            self.frame_num = 8
            self.vx = 1
            self.vy = 1

        if self.boss_state == 'Attack' and int(self.frame) >= 11:
            self.boss_state = 'Run'
            self.frame = 0
            self.frame_num = 8
            self.vx = 1
            self.vy = 1

        if self.boss_state == 'Hurt' and get_time() - self.wait_time > 0.5:
            self.boss_state = 'Run'
            self.frame = 0
            self.frame_num = 8
            self.vx = 1
            self.vy = 1

        dx = hero.x - self.x
        dy = hero.y - self.y
        dist = (dx * dx + dy * dy) ** 0.5

        if abs(dx) > abs(dy):
            self.face_dir = 4 if dx > 0 else 3
        else:
            self.face_dir = 2 if dy > 0 else 1

        # 고블린 소환
        if self.summon_started and self.summon_cool <= 0:
            self.summon_goblins()

        # 추격
        if self.boss_state == "Run":
            dx = hero.x - self.x
            dy = hero.y - self.y

            if abs(dx) > abs(dy):
                self.face_dir = 4 if dx > 0 else 3
            else:
                self.face_dir = 2 if dy > 0 else 1

        self.prev_x = self.x
        self.prev_y = self.y

        if self.damage_cool > 0:
            self.damage_cool -= game_framework.frame_time

        if self.face_dir == 1:
            self.y -= self.vy * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 2:
            self.y += self.vy * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 3:
            self.x -= self.vx * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 4:
            self.x += self.vx * RUN_SPEED_PPS * game_framework.frame_time

    def resume_after_text(self):
        self.boss_state = 'Run'
        self.frame = 0
        self.frame_num = 8
        self.vx = 1
        self.vy = 1

    def summon_goblins(self):
        self.summon_cool = 15
        for i in range(2):
            g = Goblin()
            g.x = self.x + random.randint(-80, 80)
            g.y = self.y + random.randint(-80, 80)
            game_world.add_object(g, 1)
            game_world.add_collision_pair("hero_body:goblin", game_world.hero, g)
            game_world.add_collision_pair("hero_attack:goblin", game_world.hero, g)

    def draw(self):
        cam = game_world.camera
        sx, sy = cam.world_to_screen(self.x, self.y)
        dw, dh = cam.scale_size(100, 100)

        if self.face_dir == 1:
            self.height = 64 * 3
        elif self.face_dir == 2:
            self.height = 64 * 2
        elif self.face_dir == 3:
            self.height = 64
        elif self.face_dir == 4:
            self.height = 0
        Boss.images[self.boss_state].clip_draw(int(self.frame) * 64, self.height, 64, 64, sx, sy, dw, dh)

        # hx1, hy1, hx2, hy2 = self.get_bb()
        # hx1, hy1 = cam.world_to_screen(hx1, hy1)
        # hx2, hy2 = cam.world_to_screen(hx2, hy2)
        # draw_rectangle(hx1, hy1, hx2, hy2)

    def handle_collision(self, group, other):
        if group == 'boss:wall':
            if self.face_dir == 1:  # down
                self.y = self.prev_y
            elif self.face_dir == 2:  # up
                self.y = self.prev_y
            elif self.face_dir == 3:  # left
                self.x = self.prev_x
            elif self.face_dir == 4:  # right
                self.x = self.prev_x
        if group == 'hero_attack:boss':
            if self.boss_state == 'Hurt' or self.boss_state == 'BeforeDeath':
                return
            if self.damage_cool > 0:
                return
            self.hp = self.hp - other.atk + self.defense
            self.damage_cool = 0.2
            if self.hp <= 0:
                self.boss_state = 'Death'
                self.frame = 0
                self.frame_num = 11
            else:
                self.boss_state = 'Hurt'
                self.frame = 0
                self.frame_num = 4
                self.wait_time = get_time()
        if group == 'hero_body:boss':
            if self.hp > 0:
                self.hp += 20