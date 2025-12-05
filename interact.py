from pico2d import *
import game_framework
import game_world
import dialogue_state

class InteractZone:
    def __init__(self, x, y, width, height, message="상호작용", after_message=None, give_item=None):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.message = message
        self.after_message = after_message
        self.give_item = give_item
        self.visited = False

    def get_bb(self):
        left = self.x - self.w // 2
        bottom = self.y - self.h // 2
        right = self.x + self.w // 2
        top = self.y + self.h // 2
        return left, bottom, right, top

    def interact(self):
        if not self.visited:
            dialogue_state.set_message(self.message)
            if self.give_item:
                self.give_item()
            self.visited = True
        else:
            if self.after_message:
                dialogue_state.set_message(self.after_message)
            else:
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