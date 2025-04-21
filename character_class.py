from pgzero.actor import Actor
from pgzero import keyboard
from pygame import Rect

class Character(Actor):
    def __init__(self, name, frame_count, speed):
        self.name = name
        self.frame_count = frame_count
        self.state = "idle"
        self.speed = speed
        self.actor = Actor(f"{name}idle000", (32, 32))
        self.direction = "r"
        self.timer = 0
        self.frame_index = 0
        self.on_ground = False
        self.vel_y = 0


    def draw(self):
        if self.direction == "left":
            self.actor.draw()
        else:
            self.actor.draw()
