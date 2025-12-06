from pico2d import *
import game_framework

font = None
ui = None

messages = []
msg_index = 0
on_close = None

def init():
    global font, ui, messages, msg_index
    font = load_font("Assets/DNFBitBitv2.otf", 30)
    ui = load_image("Assets/UI/message_ui.png")
    msg_index = 0

def set_message(text):
    global messages
    messages.append(text)

def handle_events():
    global msg_index, messages, on_close
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN and (e.key == SDLK_SPACE or e.key == SDLK_RETURN):
            msg_index += 1
            if msg_index >= len(messages):
                if on_close:
                    on_close()
                msg_index = 0
                messages.clear()
                game_framework.pop_mode()


def update():
    pass

def draw():
    import game_world
    game_world.render()
    ui.draw(640, 480)
    if messages:
        font.draw(90, 200, messages[msg_index], (0, 0, 0))
    update_canvas()

def pause():
    pass
def resume():
    pass
def finish():
    pass