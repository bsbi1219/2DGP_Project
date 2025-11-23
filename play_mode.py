from pico2d import *

import game_framework
import game_world

from hero import Hero
from map_1 import Map
from camera import Camera
from slime import Slime
import ui

hero = None
camera = None
map = None
ui_state = None

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
    global hero, map, camera, ui_state

    hero = Hero()
    game_world.add_object(hero, 1)

    map = Map()
    game_world.add_object(map, 0)
    game_world.map = map

    game_world.add_collision_pair('hero:wall', hero, None)
    game_world.add_collision_pair('hero:wall', None, map)

    slimes = [Slime() for _ in range(20)]
    game_world.add_objects(slimes, 1)

    game_world.add_collision_pair('hero:slime', hero, None)
    for slime in slimes:
        game_world.add_collision_pair('hero:slime', None, slime)

    camera = Camera(get_canvas_width(), get_canvas_height(), world_w = map.map_width, world_h = map.map_height, scale=6.0)
    game_world.camera = camera

    ui_state = ui.StateUI()
    game_world.add_object(ui_state, 3)

def update():
    game_world.update()
    game_world.handle_collisions()
    camera.update(hero.x, hero.y)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass