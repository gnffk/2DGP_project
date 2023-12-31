import random
import server

from pico2d import *


class FixedBackground:

    def __init__(self):
        self.image = load_image('resource/map.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        # fill here



    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = 0
        self.window_bottom = 0

    def handle_event(self, event):
        pass

