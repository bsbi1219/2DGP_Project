from pico2d import *
from hero import Hero
import game_world

running = True

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

def init():
    global hero
    global running

    running = True

    hero = Hero()
    game_world.add_object(hero, 0)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    pass