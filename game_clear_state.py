from pico2d import *
import game_framework
import title_state

name = "GameClearState"
font = None

def init():
    global font
    font = load_font('Assets/DNFBitBitv2.otf', 80)

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_RETURN or e.key == SDLK_KP_ENTER:
                game_framework.change_mode(title_state)

def update():
    pass

def draw():
    clear_canvas()
    # 검정 화면
    sw, sh = get_canvas_width(), get_canvas_height()
    draw_rectangle(0, 0, sw, sh)  # 필요 없으면 삭제해도 됨

    # 그 위에 글자
    font.draw(sw//2 - 250, sh//2, "GAME CLEAR", (255,255,255))

    update_canvas()

def pause(): pass
def resume(): pass
def finish(): pass
def exit(): pass