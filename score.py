from pico2d import load_image
import game_world
import game_framework
import hero_score_mode

class Score:
    def image_load(self):
        self.image_num[0] = load_image("resource/score/score_number(0).png")
        self.image_num[1] = load_image("resource/score/score_number(1).png")
        self.image_num[2] = load_image("resource/score/score_number(2).png")
        self.image_num[3] = load_image("resource/score/score_number(3).png")
        self.image_num[4] = load_image("resource/score/score_number(4).png")
        self.image_num[5] = load_image("resource/score/score_number(5).png")
        self.image_num[6] = load_image("resource/score/score_number(6).png")
        self.image_num[7] = load_image("resource/score/score_number(7).png")
        self.image_num[8] = load_image("resource/score/score_number(8).png")
        self.image_num[9] = load_image("resource/score/score_number(9).png")


    def __init__(self):
        self.image_num = {}
        self.image = load_image('resource/score.png')
        self.image_load()
        self.x, self.y = 800, 700
        self.score_state_hero = False
        self.score_timer_hero = 0

        self.score_state_ai = False
        self.score_timer_ai = 0

        self.score_duration = 2.0
        self.ai_score, self.hero_score = 0, 0

    def draw(self):

        self.image.clip_draw(0, 65, 800, 379, self.x, self.y, 400, 314 / 2)
        if self.score_state_hero:
            self.image.clip_draw(0, 0, 217, 65, 685, 730, 217 / 2, 65 / 2)

        if self.score_state_ai:
            self.image.clip_draw(583, 0, 800, 65, 925, 730, 217 / 2, 65 / 2)
        # hero
        if self.hero_score < 10:
            self.image_num[self.hero_score % 10].clip_draw(0, 0, 1000, 1000, 710, 680, 50, 50)
            self.image_num[0].clip_draw(0, 0, 1000, 1000, 660, 680, 50, 50)
        elif self.hero_score >= 10:
            self.image_num[self.hero_score % 10].clip_draw(0, 0, 1000, 1000, 710, 680, 50, 50)
            self.image_num[1].clip_draw(0, 0, 1000, 1000, 660, 680, 50, 50)
        # AI
        if self.ai_score < 10:
            self.image_num[self.ai_score % 10].clip_draw(0, 0, 1000, 1000, 950, 680, 50, 50)
            self.image_num[0].clip_draw(0, 0, 1000, 1000, 900, 680, 50, 50)
        elif self.hero_score < 10:
            self.image_num[self.ai_score % 10].clip_draw(0, 0, 1000, 1000, 950, 680, 50, 50)
            self.image_num[1].clip_draw(0, 0, 1000, 1000, 900, 680, 50, 50)

        pass

    def update(self):
        if self.score_state_hero:
            self.score_timer_hero += game_framework.frame_time
            game_framework.push_mode(hero_score_mode)
            if self.score_timer_hero >= self.score_duration:
                self.score_state_hero = False
                self.score_timer_hero = 0



        if self.score_state_ai:
            self.score_timer_ai += game_framework.frame_time
            if self.score_timer_ai >= self.score_duration:
                self.score_state_ai = False
                self.score_timer_ai = 0



        pass
