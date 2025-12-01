from pico2d import *
import game_framework
import game_world

def draw_outline_text(font, x, y, text, color, outline_color, thickness=2):
    for dx in (-thickness, 0, thickness):
        for dy in (-thickness, 0, thickness):
            if dx != 0 or dy != 0:
                font.draw(x + dx, y + dy, text, outline_color)
    font.draw(x, y, text, color)

class StateUI:
    def __init__(self):
        self.ui_image = load_image('Assets/UI/ui.png')
        self.hp_image = load_image('Assets/UI/2 Bars/HealthBar4.png')
        self.exp_image = load_image('Assets/UI/2 Bars/EnergyBar4.png')
        self.hero_image = load_image('Assets/icon/hero.png')

        self.coin_image = load_image('Assets/icon/icons_01.png')

        self.font = load_font('Assets/DNFBitBitv2.otf', 28)
        self.large_font = load_font('Assets/DNFBitBitv2.otf', 72)

    def draw(self):
        hero = game_world.hero

        self.ui_image.draw(250, 90)
        self.hero_image.clip_draw(0, 0, 1024, 1024, 90, 90, 100, 100)

        hp_ratio = hero.hp / hero.max_hp
        clip_width = int(32 * hp_ratio)
        draw_width = int(310 * hp_ratio)
        self.hp_image.clip_draw(0, 0, clip_width, 14, 160 + draw_width / 2, 50, draw_width, 32)

        cam_hero_x, cam_hero_y = game_world.camera.world_to_screen(hero.x, hero.y)
        clip_width = int(32 * hp_ratio)
        draw_width = int(90 * hp_ratio)
        self.hp_image.clip_draw(0, 0, clip_width, 14, cam_hero_x + draw_width / 2 - 50, cam_hero_y + 110, draw_width, 20)

        exp_ratio = hero.exp / hero.next_exp
        exp_bar_width = int(1280 * exp_ratio)
        self.exp_image.clip_draw(0, 0, exp_bar_width, 14, exp_bar_width / 2, 0, exp_bar_width, 20)

        draw_outline_text(self.font, 160, 90, f'Level: {hero.level}', (255, 255, 255), (0, 0, 0))
        draw_outline_text(self.font, 70, 930, f'{hero.gold}G', (255, 255, 255), (0, 0, 0))
        self.coin_image.draw(45, 932, 32, 32)

        if hero.dead:
            draw_outline_text(self.large_font, get_canvas_width() // 2 - 180, get_canvas_height() // 2, "YOU DIED", (255, 0, 0), (0, 0, 0))

    def update(self):
        pass

    def handle_event(self, event):
        pass

class InventoryUI:
    def __init__(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        pass