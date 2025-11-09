from pico2d import *
import game_framework
import play_mode
import game_world

name = "TitleState"
font = None
bg = None

def init():
    global font, bg
    try:
        font = load_font('Assets/DNFBitBitv2.otf', 48)
    except Exception as e:
        print('font load failed', e)
        try:
            # pico2d에서 기본 폰트 사용시 None을 못 받는 버전이 있어서 빈 문자열로 시도
            font = load_font('', 48)
        except Exception as e2:
            print('default font failed', e2)
            font = None

    try:
        bg = load_image('Assets/Grow or Die title.png')
    except Exception as e:
        print('bg load failed', e)
        bg = None

def draw_text_with_outline(font, x, y, text, color, outline_color, thickness=2):
    for dx in (-thickness, 0, thickness):
        for dy in (-thickness, 0, thickness):
            if dx != 0 or dy != 0:
                font.draw(x + dx, y + dy, text, outline_color)
    font.draw(x, y, text, color)

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_RETURN or e.key == SDLK_KP_ENTER:
                game_framework.change_mode(play_mode)
            elif e.key == SDLK_ESCAPE:
                game_framework.quit()

def update():
    pass

def draw():
    clear_canvas()
    if bg:
        bg.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    sw, sh = get_canvas_width(), get_canvas_height()
    if font:
        draw_text_with_outline(font, sw // 2 - 290, sh // 2 - 160, "Press Enter to Start", (0, 0, 0), (0, 0, 0), 4)
        draw_text_with_outline(font, sw//2 - 170, sh//2 - 250, "Esc to Quit", (0, 0, 0), (0, 0, 0), 4)
        font.draw(sw//2 - 290, sh//2 - 160, "Press Enter to Start", (255,255,255))
        font.draw(sw//2 - 170, sh//2 - 250, "Esc to Quit", (255,255,255))
    else:
        # 폰트 없으면 텍스트 건너뛰거나 간단한 안내 이미지로 대체
        pass
    update_canvas()

def pause(): pass
def resume(): pass

def exit():
    global font, bg
    font = None
    bg = None

def finish():
    game_world.clear()