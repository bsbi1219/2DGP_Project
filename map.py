import csv
from pico2d import *

# class Map:
#     def __init__(self):
#         self.floor_image = load_image('Assets/dungeon/walls_floor.png')
#         self.wall_image = load_image('Assets/dungeon/walls_floor.png')
#         self.tile_size = 16
#         self.map_1_floor = []
#         self.map_1_wall = []
#
#         with open('csv/맵 1번._바닥.csv', 'r') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 self.map_1_floor.append([int(x) for x in row])
#         with (open('csv/맵 1번._벽.csv', 'r') as f):
#             reader = csv.reader(f)
#             for row in reader:
#                 self.map_1_wall.append([int(x) for x in row])
#
#     def draw_map(self, height, map_list, map_image):
#         for y in range(height):
#             for x in range(len(map_list[y])):
#                 tile = map_list[y][x]
#                 if tile == 0: continue
#                 map_image.clip_draw((tile % 13) * 16, (tile % 23) * 16, 16, 16,
#                                          x * self.tile_size + self.tile_size / 2,
#                                          (height - y - 1) * self.tile_size + self.tile_size / 2)
#
#     def draw(self):
#         height_floor = len(self.map_1_floor)
#         height_wall = len(self.map_1_wall)
#         self.draw_map(height_floor, self.map_1_floor, self.floor_image)
#         self.draw_map(height_wall, self.map_1_wall, self.wall_image)
#
#     def update(self):
#          pass

# python
class Map:
    def __init__(self):
        from pico2d import load_image
        import csv
        self.floor_image = load_image('Assets/dungeon/walls_floor.png')
        self.wall_image = load_image('Assets/dungeon/walls_floor.png')
        self.tile_size = 16
        self.map_1_floor = []
        self.map_1_wall = []

        with open('csv/맵 1번._바닥.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.map_1_floor.append([int(x) for x in row])
        with open('csv/맵 1번._벽.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.map_1_wall.append([int(x) for x in row])

    def draw_map(self, height, map_list, map_image):
        cols = map_image.w // self.tile_size
        image_h = map_image.h
        for y in range(height):
            for x in range(len(map_list[y])):
                tile = map_list[y][x]
                # if tile == 0:
                #     continue
                idx = tile  # CSV가 1부터 시작하면 -1; 0부터면 이 줄 제거
                if idx < 0:
                    continue
                sx = (idx % cols) * self.tile_size
                # 타일셋이 위쪽부터 번호인 경우(에디터 기준) 아래 보정:
                sy = image_h - (idx // cols + 1) * self.tile_size
                map_image.clip_draw(sx, sy, self.tile_size, self.tile_size,
                                    x * self.tile_size + self.tile_size / 2,
                                    (height - y - 1) * self.tile_size + self.tile_size / 2)

    def draw(self):
        height_floor = len(self.map_1_floor)
        height_wall = len(self.map_1_wall)
        self.draw_map(height_floor, self.map_1_floor, self.floor_image)
        self.draw_map(height_wall, self.map_1_wall, self.wall_image)

    def update(self):
        pass
