from pico2d import open_canvas, delay, close_canvas
import game_framework
from camera import Camera

import play_mode as start_mode

open_canvas(1280, 960)
game_framework.run(start_mode)
close_canvas()