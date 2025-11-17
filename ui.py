from pico2d import *
import game_framework
import game_world

class StateUI:
    def __init__(self):
        self.image = load_image('Assets/UI/ui.png')

    def draw(self):
        self.image.draw(250, 90)

    def update(self):
        pass

    def handle_event(self, event):
        pass

class InventoryUI:
    def __init__(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        pass