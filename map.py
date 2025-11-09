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

        width = 80
        height = 60

        self.map_1_data = [] # 바닥
        self.map_2_data = [] # 벽

        # 1은 바닥, 2는 벽 왼, 3은 벽 가운데, 4는 벽 오. 5는 왼벽, 6은 오른벽
        for y in range(height):
            row_floor = []
            row_wall = []
            for x in range(width):
                floor = 1
                wall = 0
                if x == 0 and y == 0:
                    wall = 2
                elif x == 0 and y > 1:
                    wall = 5
                elif x == width - 1 and y > 1:
                    wall = 5
                elif x == width - 1 and y == 0:
                    wall = 4
                elif y == 0:
                    wall = 3
                row_floor.append(floor)
                row_wall.append(wall)
            self.map_1_data.append(row_floor)
            self.map_2_data.append(row_wall)

    # 가로 13개 세로 23개 타일
    def draw(self):
        for y in range(len(self.map_1_data)):
            for x in range(len(self.map_1_data[y])):
                tile = self.map_1_data[y][x]
                if tile == 1:
                    self.map_image.clip_draw(16 * 1, 16 * 16, self.map_tile_size, self.map_tile_size, x * self.map_tile_size + self.map_tile_size / 2,
                                               (len(self.map_1_data) - y - 1) * self.map_tile_size + self.map_tile_size / 2, 16, 16)
        for y in range(len(self.map_2_data)):
            for x in range(len(self.map_2_data[y])):
                tile = self.map_2_data[y][x]
                if tile == 2:
                    self.map_image.clip_draw(16 * 0, 16 * 18, self.map_tile_size, self.map_tile_size * 5, x * self.map_tile_size + self.map_tile_size / 2,
                                               (len(self.map_2_data) - y - 1) * self.map_tile_size + self.map_tile_size / 2 - 16 * 2, 16, 16 * 5)
                if tile == 3:
                    self.map_image.clip_draw(16 * 1, 16 * 18, self.map_tile_size, self.map_tile_size * 5, x * self.map_tile_size + self.map_tile_size / 2,
                                               (len(self.map_2_data) - y - 1) * self.map_tile_size + self.map_tile_size / 2 - 16 * 2, 16, 16 * 5)
                if tile == 4:
                    self.map_image.clip_draw(16 * 2, 16 * 18, self.map_tile_size, self.map_tile_size * 5, x * self.map_tile_size + self.map_tile_size / 2,
                                               (len(self.map_2_data) - y - 1) * self.map_tile_size + self.map_tile_size / 2 - 16 * 2, 16, 16 * 5)
                if tile == 5:
                    self.map_image.clip_draw(16 * 2, 16 * 3, self.map_tile_size, self.map_tile_size, x * self.map_tile_size + self.map_tile_size / 2,
                                               (len(self.map_2_data) - y - 1) * self.map_tile_size + self.map_tile_size / 2 - 16, 16, 16)

    def update(self):
        pass