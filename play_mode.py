from pico2d import *

import game_framework
import game_world

from hero import Hero

hero = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            hero.handle_event(event)

def init():
    global hero

    hero = Hero()
    game_world.add_object(hero, 1)


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    pass

def pause(): pass
def resume(): pass