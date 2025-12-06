import csv
import game_world
from pico2d import *

def f_read(filename, map_list):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            map_list.append([int(x) for x in row])


class Map:
    def __init__(self):
        from pico2d import load_image
        self.floor_wall_image = load_image('Assets/dungeon/walls_floor.png')
        self.object_cave_image = load_image('Assets/objects/Cave_objects_source.png')
        self.object_web_image = load_image('Assets/objects/web.png')
        self.tile_size = 16
        self.map_2_floor = []
        self.map_2_wall = []
        self.map_2_object_cave = []
        self.map_2_object_wep = []
        self.collision_rects = []

        f_read('csv/맵 2번_바닥.csv', self.map_2_floor)
        f_read('csv/맵 1번_벽.csv', self.map_2_wall)
        f_read('csv/맵 1번_동굴 오브젝트.csv', self.map_2_object_cave)
        f_read('csv/맵 1번_거미줄.csv', self.map_2_object_wep)

        if len(self.map_2_floor) == 0:
            raise Exception("맵 바닥 CSV를 읽지 못했음")
        self.map_width = len(self.map_2_floor[0]) * self.tile_size
        self.map_height = len(self.map_2_floor) * self.tile_size

        with open('csv/맵 2번.tmj', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for layer in data['layers']:
            if layer['type'] == 'objectgroup':
                for obj in layer['objects']:
                    x = obj['x']
                    y = obj['y']
                    w = obj['width']
                    h = obj['height']

                    left = x
                    right = x + w
                    bottom = self.map_height - (y + h)
                    top = self.map_height - y

                    self.collision_rects.append((left, bottom, right, top))

    def draw_map(self, height, map_list, map_image, camera):
        cols = map_image.w // self.tile_size
        image_h = map_image.h

        for y in range(height):
            for x in range(len(map_list[y])):
                idx = map_list[y][x]
                if idx < 0:
                    continue

                sx = (idx % cols) * self.tile_size
                sy = image_h - (idx // cols + 1) * self.tile_size

                wx = x * self.tile_size + self.tile_size / 2
                wy = (height - y - 1) * self.tile_size + self.tile_size / 2

                camera.draw_image(
                    map_image,
                    sx, sy,
                    self.tile_size, self.tile_size,
                    wx, wy,
                    self.tile_size, self.tile_size
                )

    def draw(self):
        cam = game_world.camera
        height_floor = len(self.map_2_floor)
        height_wall = len(self.map_2_wall)
        height_object_cave = len(self.map_2_object_cave)
        height_object_wep = len(self.map_2_object_wep)
        self.draw_map(height_floor, self.map_2_floor, self.floor_wall_image, cam)
        self.draw_map(height_wall, self.map_2_wall, self.floor_wall_image, cam)
        self.draw_map(height_object_cave, self.map_2_object_cave, self.object_cave_image, cam)
        self.draw_map(height_object_wep, self.map_2_object_wep, self.object_web_image, cam)

        for rect in self.collision_rects:
            l, b, r, t = rect
            sx1, sy1 = cam.world_to_screen(l, b)
            sx2, sy2 = cam.world_to_screen(r, t)
            draw_rectangle(sx1, sy1, sx2, sy2)

    def update(self):
        pass
