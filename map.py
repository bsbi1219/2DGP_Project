from pico2d import *

class Map:
    def __init__(self):
        self.wall_image = load_image('Assets/dungeon/decorative_cracks_walls.png')
        self.door_image = load_image('Assets/dungeon/door_lever_chest_animation.png')
        self.floor_image = load_image('Assets/dungeon/decorative_cracks_floor.png')
        self.fire_image = load_image('Assets/dungeon/fire_animation.png')
        self.objects_image = load_image('Assets/dungeon/Objects.png')

        self.wall_fw = 128
        self.wall_fh = 512
        self.wall_w = 16
        self.wall_h = 16

        self.floor_fw = 128
        self.floor_fh = 240
        self.floor_w = 16
        self.floor_h = 16

        self.door_fw = 160
        self.door_fh = 192
        self.door_w = 32
        self.door_h = 32

        self.fire_fw = 176
        self.fire_fh = 288
        self.fire_w = 44
        self.fire_h = 48

    def draw(self):
        self.image.draw(640, 480)