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

        width = 76
        height = 56

        self.map_1_data = []

        # 1은 바닥, 2는 벽
        for y in range(height):
            row = []
            for x in range(width):
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    row.append(2)  # 벽
                else:
                    row.append(1)  # 바닥
            self.map_1_data.append(row)

    def draw(self):
        for y in range(len(self.map_1_data)):
            for x in range(len(self.map_1_data[y])):
                tile = self.map_1_data[y][x]
                if tile == 1:
                    self.map_image.clip_draw(0 + 16 * 1, 0 + 16 * 16, self.map_tile_size, self.map_tile_size, x * self.map_tile_size + self.map_tile_size / 2,
                                               (len(self.map_1_data) - y - 1) * self.map_tile_size + self.map_tile_size / 2, 16, 16)

    def update(self):
        pass