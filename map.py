from pico2d import *

class Map:
    def __init__(self):
        self.map_image = load_image('Assets/dungeon/walls_floor.png')
        self.fire_image = load_image('Assets/dungeon/fire_animation.png')
        self.objects_image = load_image('Assets/dungeon/Objects.png')

        self.map_fw = 208
        self.map_fh = 368
        self.map_tile_size = 16

        self.fire_fw = 176
        self.fire_fh = 288
        self.fire_w = 44
        self.fire_h = 48

        # 1은 바닥, 2는 벽
        self.map_1_data = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 0, 0, 0, 0, 0, 0, 1, 2],
            [2, 1, 0, 0, 0, 0, 0, 0, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def draw(self):
        for y in range(len(self.map_1_data)):
            for x in range(len(self.map_1_data[y])):
                tile = self.map_1_data[y][x]
                if tile == 1:
                    self.floor_image.clip_draw(0, 0 + 16 * 8, self.floor_w, self.floor_h,
                                               x * self.floor_w + self.floor_h / 2,
                                               (len(self.map_1_data) - y - 1) * self.floor_w + self.floor_h / 2)
                elif tile == 2:
                    self.floor_image.clip_draw(16, 0, self.tile_size, self.tile_size,
                                               x * self.tile_size + self.tile_size / 2,
                                               (len(self.map_data) - y - 1) * self.tile_size + self.tile_size / 2)