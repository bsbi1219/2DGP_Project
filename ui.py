from pico2d import *
import game_framework
import game_world

class StateUI:
    def __init__(self):
        self.ui_image = load_image('Assets/UI/ui.png')
        self.hp_image = load_image('Assets/UI/2 Bars/HealthBar4.png')
        self.hero_image = load_image('Assets/icon/hero.png')

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