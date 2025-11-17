import csv
import game_world
import json
from pico2d import *

# 가로 13개, 세로 23개 타일

def f_read(filename, map_list):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            map_list.append([int(x) for x in row])


class Map:
    def __init__(self):
        from pico2d import load_image
        import csv
        self.floor_image = load_image('Assets/dungeon/walls_floor.png')
        self.wall_image = load_image('Assets/dungeon/walls_floor.png')
        self.object_cave_image = load_image('Assets/objects/Cave_objects_source.png')
        self.object_web_image = load_image('Assets/objects/web.png')
        self.object_spider_image = load_image('Assets/objects/Objects.png')
        self.object_image = load_image('Assets/dungeon/Objects.png')
        self.tile_size = 16
        self.map_1_floor = []
        self.map_1_wall = []
        self.map_1_objects = []
        self.map_1_object_cave = []
        self.map_1_object_spider = []
        self.map_1_object_wep = []
        self.collision_rects = []

        f_read('csv/맵 1번_바닥.csv', self.map_1_floor)
        f_read('csv/맵 1번_벽.csv', self.map_1_wall)
        f_read('csv/맵 1번_던전 오브젝트.csv', self.map_1_objects)
        f_read('csv/맵 1번_거미 여왕 맵 오브젝트_cave.csv', self.map_1_object_cave)
        f_read('csv/맵 1번_거미 여왕 맵 오브젝트_spider.csv', self.map_1_object_spider)
        f_read('csv/맵 1번_거미 여왕 맵 오브젝트_web.csv', self.map_1_object_wep)

        if len(self.map_1_floor) == 0:
            raise Exception("맵 바닥 CSV를 읽지 못했음")
        self.map_width = len(self.map_1_floor[0]) * self.tile_size
        self.map_height = len(self.map_1_floor) * self.tile_size

        with open('csv/맵 1번.tmj', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for layer in data['layers']:
            if layer['type'] == 'objectgroup':
                for obj in layer['objects']:
                    if obj.get('properties'):
                        props = {p['name']: p['value'] for p in obj['properties']}
                        if props.get('collidable', False):
                            y = self.map_height - obj['y'] - obj['height']
                            left = obj['x']
                            bottom = y
                            right = left + obj['width']
                            top = bottom + obj['height']
                            rect = (left, bottom, right, top)
                            self.collision_rects.append(rect)

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
        height_floor = len(self.map_1_floor)
        height_wall = len(self.map_1_wall)
        height_object = len(self.map_1_objects)
        height_object_cave = len(self.map_1_object_cave)
        height_object_spider = len(self.map_1_object_spider)
        height_object_wep = len(self.map_1_object_wep)
        self.draw_map(height_floor, self.map_1_floor, self.floor_image, cam)
        self.draw_map(height_wall, self.map_1_wall, self.wall_image, cam)
        self.draw_map(height_object, self.map_1_objects, self.object_image, cam)
        self.draw_map(height_object_cave, self.map_1_object_cave, self.object_cave_image, cam)
        self.draw_map(height_object_spider, self.map_1_object_spider, self.object_spider_image, cam)
        self.draw_map(height_object_wep, self.map_1_object_wep, self.object_web_image, cam)


    def update(self):
        pass
