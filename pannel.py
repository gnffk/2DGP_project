from pico2d import *
import server

class Pannel:
    def __init__(self):
        self.image = load_image('resource/score.png')

    def draw(self):
        self.image.draw(500, 500)

    def update(self):
        pass

    def handle_event(self, event):
        pass