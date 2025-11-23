from pico2d import *
import game_framework
import game_world

class StateUI:
    def __init__(self):
        self.ui_image = load_image('Assets/UI/ui.png')
        self.hp_image = load_image('Assets/UI/2 Bars/HealthBar4.png')

    def draw(self):
        hero = game_world.hero
        self.ui_image.draw(250, 90)
        hp_ratio = hero.hp / hero.max_hp
        clip_width = int(32 * hp_ratio)
        draw_width = int(310 * hp_ratio)

        # 왼쪽 끝을 116으로 고정 (180 - 64 = 116)
        self.hp_image.clip_draw(0, 0, clip_width, 14, 160 + draw_width / 2, 50, draw_width, 32)

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