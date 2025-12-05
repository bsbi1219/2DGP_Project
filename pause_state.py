from pico2d import *
import game_framework
import game_world

pause_image = None

def init():
    pass

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN and e.key == SDLK_p:
            game_framework.pop_mode()

def update():
    pass

def draw():
    pass

def pause():
    pass

def resume():
    pass

def finish():
    pass