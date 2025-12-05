from pico2d import *
import game_framework
import game_world
import dialogue_state

class InteractZone:
    def __init__(self, x, y, width, height, message="상호작용"):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.message = message

    def get_bb(self):
        left = self.x - self.w // 2
        bottom = self.y - self.h // 2
        right = self.x + self.w // 2
        top = self.y + self.h // 2
        return left, bottom, right, top

    def interact(self):
        # 상호작용 시 대화창 띄우기
        dialogue_state.set_message(self.message)
        game_framework.push_mode(dialogue_state)

    def draw(self):
        # 디버그용 (필요할 때만 호출)
        l, b, r, t = self.get_bb()
        cam = game_world.camera
        sx1, sy1 = cam.world_to_screen(l, b)
        sx2, sy2 = cam.world_to_screen(r, t)
        draw_rectangle(sx1, sy1, sx2, sy2)

    def update(self):
        pass