from pico2d import *
import game_framework
import game_world

store_ui = None

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

        self.small_font = load_font('Assets/DNFBitBitv2.otf', 16)
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

        draw_outline_text(self.small_font, 350, 125, f'HP {hero.hp}/{hero.max_hp}', (255, 255, 255), (0, 0, 0))
        draw_outline_text(self.small_font, 350, 105, f'ATK +{hero.atk}', (255, 255, 255), (0, 0, 0))
        draw_outline_text(self.small_font, 350, 85, f'DEF +{hero.defense}', (255, 255, 255), (0, 0, 0))

        draw_outline_text(self.font, 160, 90, f'Level: {hero.level}', (255, 255, 255), (0, 0, 0))
        draw_outline_text(self.font, 70, 930, f'{hero.gold}G', (255, 255, 255), (0, 0, 0))
        self.coin_image.draw(45, 932, 32, 32)

        draw_outline_text(self.small_font, 1150, 40, f'EXP : {hero.exp}/{hero.next_exp}', (255, 255, 255), (0, 0, 0))

        if hero.dead:
            draw_outline_text(self.large_font, get_canvas_width() // 2 - 180, get_canvas_height() // 2, "YOU DIED", (255, 0, 0), (0, 0, 0))
            draw_outline_text(self.font, get_canvas_width() // 2 - 180, get_canvas_height() // 2 - 50, f'사망 횟수 : {hero.death_count}',(255, 255, 255), (0, 0, 0))

    def update(self):
        pass

    def handle_event(self, event):
        pass

class StoreUI:
    def __init__(self):
        global store_ui
        store_ui = load_image('Assets/UI/store_ui.png')

    def init(self):
        pass

    def draw(self):
        game_world.render()
        store_ui.draw(640, 480)
        update_canvas()

    def update(self):
        pass

    def handle_events(self):
        events = get_events()
        for e in events:
            self.handle_event(e)

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, event.y
            my = get_canvas_height() - my
            hero = game_world.hero
            if 810 < mx < 873 and 705 < my < 770:
                game_framework.pop_mode()
                return
            if 417 < mx < 863 and 563 < my < 653:
                if hero.gold < 30:
                    print("돈 부족!")
                    return
                hero.gold -= 30
                hero.get_potion()
                return
            if 417 < mx < 863 and 455 < my < 545:
                if hero.gold < 70:
                    print("돈 부족!")
                    return
                hero.gold -= 70
                hero.get_hp(10)
                return
            if 417 < mx < 863 and 347 < my < 437:
                if hero.gold < 80:
                    print("돈 부족!")
                    return
                hero.gold -= 80
                hero.get_atk(5)
                hero.get_def(5)
                return
            if 417 < mx < 863 and 232 < my < 322:
                if hero.gold < 250:
                    print("돈 부족!")
                    return
                hero.gold -= 250
                hero.get_exp(hero.next_exp)
                return

    def get_bb(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def finish(self):
        pass