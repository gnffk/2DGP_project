from pico2d import *
import server

class Pannel:
    def __init__(self):
        self.image = load_image('resource/lecture/win.png')
        self.image_point_match = load_image('resource/lecture/pointmatch.png')
        self.image_final_win = load_image('resource/lecture/final_win.png')
        self.image_lose = load_image('resource/lecture/lose.png')
        self.image_ready = load_image('resource/lecture/ready.png')
        self.image_go = load_image('resource/lecture/go.png')
        self.turn =1
    def draw(self):
        if server.score.ai_score == 10 or server.score.hero_score ==10:
            self.image_point_match.draw(800,400)
        if server.score.ai_score == 11:
            self.image_lose.draw(800,400)
        if server.score.ai_score == 11:
            self.image_final_win.draw(800, 400)


        else:
            self.image.draw(800, 400)


    def update(self):

        pass

    def handle_event(self, event):
        pass