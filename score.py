from pico2d import load_image
import game_world
import game_framework


class Score:
    def __init__(self):
        self.image = load_image('resource/score.png')
        self.x , self.y = 800,700
    def draw(self):

        self.image.clip_draw( 0,65, 800, 379,self.x,self.y,400,314/2)

        pass
    def update(self):
        pass

