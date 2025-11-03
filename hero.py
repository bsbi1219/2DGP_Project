from pico2d import *
import game_world

class Hero:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.image = load_image('Assets/hero/hero_idle.png')

    def draw(self):
        self.image.draw(self.x, self.y)