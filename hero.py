from pico2d import *
import game_world
from state_machine import StateMachine

class Idle:
    def __init__(self, hero):
        self.hero = hero

class Hero:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.face_dir = 1
        self.image = load_image('Assets/hero/hero_idle.png')
        self.IDLE = Idle(self)

        self.state_machine = StateMachine(self.IDLE,{ })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()