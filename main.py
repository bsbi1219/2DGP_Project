from pico2d import *
from play_mode import *

open_canvas()
init()
while running:
    handle_events()
    update()
    draw()
    delay(0.01)
finish()
close_canvas()