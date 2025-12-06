from pico2d import *
import game_framework

font = None
ui = None
message = ""

def init():
    global font, ui
    font = load_font("Assets/DNFBitBitv2.otf", 30)
    ui = load_image("Assets/UI/message_ui.png")

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
    ui.draw(640, 480)
    font.draw(90, 200, message, (0, 0, 0))
    update_canvas()

def pause():
    pass
def resume():
    pass
def finish():
    pass