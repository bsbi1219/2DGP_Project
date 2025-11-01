from pico2d import *

class Hero:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.image = load_image('hero.png')

    def draw(self):
        self.image.draw(self.x, self.y)