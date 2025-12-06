from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Sheep:
    image = None

    def __init__(self):
        if Sheep.image is None:
            Sheep.image = load_image("Assets/animal/sheep.png")
        self.x = 215
        self.y = 307
        self.frame = 0

    def update(self):
        ft = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * ft) % 3

    def draw(self):
        cam = game_world.camera
        sx, sy = cam.world_to_screen(self.x, self.y)
        dw, dh = cam.scale_size(32, 32)
        self.image.clip_draw(int(self.frame) * 32, 96, 32, 32, sx, sy, dw, dh)

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8