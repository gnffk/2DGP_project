from pico2d import load_image
import game_world
import game_framework


class Score:
    def image_load(self):
        self.image_num = {}
        for n in range(10):
            self.image_num[n] = [load_image("resource/score/number"+"(%d)" % i + ".png") for i in range(0, 10)]
    def __init__(self):
        self.image = load_image('resource/score.png')
        self.image_load()
        self.x , self.y = 800,700
        self.score_state = False
        self.score_timer = 0
        self.score_duration = 2.0
        self.ai_score, self.hero_score = 0,0

    def draw(self):

        self.image.clip_draw( 0,65, 800, 379,self.x,self.y,400,314/2)
        if self.score_state:
            self.image.clip_draw(0, 0, 217, 65, 685, 730, 217/2, 65/2)

        self.image_num[self.ai_score].clip_draw( 0,0, 1000, 1000,700,700,100,100)
        pass
    def update(self):
        if self.score_state:
            self.score_timer += game_framework.frame_time
            if self.score_timer >= self.score_duration:
                self.score_state = False
                self.score_timer = 0
        pass

