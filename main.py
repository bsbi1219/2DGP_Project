from pico2d import open_canvas, delay, close_canvas
import game_framework
import title_state

import play_mode as start_mode

open_canvas(1280, 960)
game_framework.run(title_state)
close_canvas()