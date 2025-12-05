from pico2d import *

import game_framework
import game_world

from hero import Hero
from map_1 import Map
from camera import Camera
from slime import Slime
from goblin import Goblin
from wall import Wall
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            import pause_state
            game_framework.push_mode(pause_state)
        else:
            hero.handle_event(event)

def init():
    global hero, map, camera, ui_state

    hero = Hero()
    game_world.add_object(hero, 1)
    game_world.hero = hero

    map = Map()
    game_world.add_object(map, 0)
    game_world.map = map

    # 슬라임
    game_world.add_collision_pair('slime:wall', None, None)
    slimes = [Slime() for _ in range(20)]
    game_world.add_objects(slimes, 1)
    for slime in slimes:
        game_world.add_collision_pair('slime:wall', slime, None)

    # 고블린
    game_world.add_collision_pair('goblin:wall', None, None)
    goblins = [Goblin() for _ in range(20)]
    game_world.add_objects(goblins, 1)
    for goblin in goblins:
        game_world.add_collision_pair('goblin:wall', goblin, None)

    # Hero와 충돌 처리
    game_world.add_collision_pair('hero_body:slime', hero, None)
    game_world.add_collision_pair('hero_attack:slime', hero, None)
    for slime in slimes:
        game_world.add_collision_pair('hero_body:slime', None, slime)
        game_world.add_collision_pair('hero_attack:slime', None, slime)

    game_world.add_collision_pair('hero_body:goblin', hero, None)
    game_world.add_collision_pair('hero_attack:goblin', hero, None)
    for goblin in goblins:
        game_world.add_collision_pair('hero_body:goblin', None, goblin)
        game_world.add_collision_pair('hero_attack:goblin', None, goblin)

    # 벽과 충돌 처리
    game_world.add_collision_pair('hero_body:wall', hero, None)
    for rect in map.collision_rects:
        left, bottom, right, top = rect
        wall = Wall(left, bottom, right, top)
        game_world.add_object(wall, 0)
        game_world.add_collision_pair('hero_body:wall', None, wall)
        game_world.add_collision_pair('slime:wall', None, wall)
        game_world.add_collision_pair('goblin:wall', None, wall)

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