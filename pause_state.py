from pico2d import *
import game_framework
import game_world

font = None

def init():
    global font
    font = load_font('Assets/DNFBitBitv2.otf', 70)

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN and e.key == SDLK_p:
            game_framework.pop_mode()

def update():
    pass

def draw():
    game_world.render()
    sx, sy = game_world.camera.world_to_screen(640, 480)
    font.draw(sx - 140, sy, "일시정지", (255, 255, 255))

def pause():
    pass

def resume():
    pass

def finish():
    pass