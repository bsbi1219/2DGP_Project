from pico2d import *

import game_framework
import game_world

from hero import Hero
from map_1 import Map
from camera import Camera

hero = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            hero.handle_event(event)

def init():
    global hero

    hero = Hero()
    game_world.add_object(hero, 1)

    map = Map()
    game_world.add_object(map, 0)

    cam = Camera(get_canvas_width(), get_canvas_height(), world_w=None, world_h=None, scale=2.0)


def update():
    game_world.update()
    game_world.handle_collisions()
    cam.update(hero.x, hero.y)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass