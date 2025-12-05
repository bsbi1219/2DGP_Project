from pico2d import *
from OpenGL.GL import glLoadIdentity
from OpenGL.GLU import gluOrtho2D
import game_framework

font = None
ui = None
message = ""

def init():
    global font
    font = load_font("Assets/DNFBitBitv2.otf", 20)

def set_message(text):
    global message
    message = text

def handle_events():
    events = get_events()
    for e in events:
        # 스페이스 or 엔터 누르면 대화 종료
        if e.type == SDL_KEYDOWN and (e.key == SDLK_SPACE or e.key == SDLK_RETURN):
            game_framework.pop_mode()

def update():
    pass

def draw():
    import game_world
    game_world.render()
    font.draw(100, 300, message, (255, 255, 255))
    # 캔버스를 업데이트해 화면에 표시
    update_canvas()

def pause():
    pass
def resume():
    pass
def finish():
    pass