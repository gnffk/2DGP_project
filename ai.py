from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode

import server

# A Run Speed
PIXEL_PER_METER= (10.0/0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS* PIXEL_PER_METER)
# Boy Action Speed
# fill here
TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11
animation_names = ['attack_middle', 'attack_up','defence',
                   'Idle','run','run_back','score']
class AI:
    images = None
    def load_images(self):
        if AI.images == None:
            AI.images = {}
            for name in animation_names:
                AI.images[name] = [load_image("resource/" + name + ".png") ]
    def __init__(self):
        self.x = 980
        self.y = 150
        self.weapon_x, self.weapon_y = 850, 230
        self.size_x = 500
        self.size_y = 348
        self.load_images()
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = 0
        self.state = 'Idle'
        self.attack_up_cooldown = 0
        self.attack_middle_cooldown = 0
        self.defence_cooldown = 0
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()
        self.count = 0
    def get_bb(self):
        return self.x + 30, self.y - 100, self.x + 110, self.y + 90 #충돌 박스 크기 x = 90 / y = 190
    def get_aa(self):
        return self.weapon_x, self.weapon_y, self.weapon_x+ 14, self.weapon_y + 14
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()
        if self.x > 1600 - 90:
            self.x = 1600 - 90
            self.weapon_x = self.x - 120
            self.weapon_y = self.y + 80
    def draw(self):
        image = AI.images[self.state][0]  # 가져온 이미지 리스트에서 첫 번째 이미지를 사용
        image.clip_draw(int(self.frame) * 500, 0 * 348, 500, 348, self.x, self.y)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_aa())
        if self.x - server.hero.x < 100:
            self.x = server.hero.x + 100
            self.weapon_x = self.x - 120
            self.weapon_y = self.y + 80
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass
    def score_not_equal_condition(self):
        if server.score.ai_score != server.score.hero_score:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c1
    def score_less_score_condition(self):
        if server.score.ai_score < server.score.hero_score:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c2
    def score_not_meet_condition(self):
        if self.x- server.hero.x > 100:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c3
    def score_meet_condition(self):
        if self.x- server.hero.x <= 100:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c4
    def ai_defecne_time_up_condition(self):
        if self.defence_cooldown >0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c5
    def ai_defecne_time_zero_condition(self):
        if self.defence_cooldown ==0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c6
    def hero_attack_condition(self):
        if server.hero.state == 'Attack':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c7
    def ai_attack_time_zero_condition(self):
        if self.attack_up_cooldown == 0 or self.attack_middle_cooldown ==0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c8
    def ai_one_attack_time_zero_condition(self):
        if (self.attack_up_cooldown != 0 and self.attack_middle_cooldown ==0) or (self.attack_up_cooldown == 0 and self.attack_middle_cooldown !=0):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c9
    def score_more_score_condition(self):
        if server.score.ai_score > server.score.hero_score:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c10
    def distance_less_than(self):
        if self.x - server.hero.x < 350:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c11
    def distance_more_than(self):
        if self.x - server.hero.x >= 350:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c12
    def score_more_score_condition(self):
        if server.score.ai_score > server.score.hero_score:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c13
    def hero_attack_time_zero_condition(self):
        if server.hero.attack_up_cooldown ==0 or server.hero.attack_middle_cooldown==0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c14
    def hero_attack_time_zero_not_condition(self):
        if server.hero.attack_up_cooldown !=0 or server.hero.attack_middle_cooldown!=0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c15
    def score_equal_conditon(self):
        if server.score.ai_score == server.score.hero_score:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass #c16

    def front_Move(self):
        if self.state != 'run':
            self.frame = 0
            self.state = 'run'
        self.speed = RUN_SPEED_PPS

        self.x -= self.speed * game_framework.frame_time
        self.weapon_x -= RUN_SPEED_PPS * game_framework.frame_time
        if self.frame >= 10.9:
            self.frame = 0
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def back_Move(self):
        if self.state != 'run_back':
            self.frame = 0
            self.state = 'run_back'
        self.speed = RUN_SPEED_PPS

        self.x += self.speed * game_framework.frame_time
        self.weapon_x += RUN_SPEED_PPS * game_framework.frame_time
        if self.frame >= 10.9:
            self.frame = 0
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def defence(self):
        if self.state != 'defence':
            self.frame = 0
            self.state = 'defence'

            pass

        if self.frame >= 10.9:
            self.frame = 0
            self.state = 'Idle'
            print('end')
            return BehaviorTree.SUCCESS
        else:

            return BehaviorTree.RUNNING
        pass  # a3

    def middle_attack(self):
        if self.state != 'attack_middle':
            self.frame = 0
            self.state = 'attack_middle'

            pass
        if server.score.score_state_ai == False:
            if self.frame <= 5.5:
                self.weapon_x -= RUN_SPEED_PPS * game_framework.frame_time / 2
                pass
            elif self.frame > 5.5:
                self.weapon_x += RUN_SPEED_PPS * game_framework.frame_time /2
                pass
        if self.frame >= 10.9:
            self.frame = 0
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
            pass  # a4

    def up_attack(self):
        if self.state != 'attack_up':
            self.frame = 0
            self.state = 'attack_up'

            pass
        if server.score.score_state_ai == False:
            if self.frame <= 5.5:
                self.weapon_x -= RUN_SPEED_PPS * game_framework.frame_time / 2
                pass
            elif self.frame > 5.5:
                self.weapon_x += RUN_SPEED_PPS * game_framework.frame_time
                pass

        if self.frame >= 10.9:
            self.frame = 0
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
            pass  # a5

    def idle(self):
        if self.state != 'Idle':
            self.frame = 0
            self.state = 'Idle'

        if self.frame >= 10.9:
            self.frame = 0
            self.state = 'Idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass  # a6
    def handle_collision(self, group, other):
        if group == 'ai:hero':
            if server.hero.state != 'defence': #defence 일때는 공격 추가 안됨
                server.score.score_state_ai = True
                server.score.ai_score += 1
                self.x = server.hero.x + 100
                self.weapon_x = self.x - 120
                self.weapon_y = self.y + 80

            #print("찌름")
            pass
    def build_behavior_tree(self):
        c1 = Condition('점수가 안똑같음?', self.score_not_equal_condition)
        c2 = Condition('점수가 적음?', self.score_less_score_condition)
        c3 = Condition('못만남?', self.score_not_meet_condition)
        c4 = Condition('만남?',self.score_meet_condition )
        c5 = Condition('방어 쿨타임 0이상인가?',self.ai_defecne_time_up_condition)
        c6 = Condition('방어 쿨타임이 0인가',self.ai_defecne_time_zero_condition)
        c7 = Condition('상대방이 공격중인가?', self.hero_attack_condition)
        c8 = Condition('둘중에 하나라도 AI 공격쿨타임이 0인가?', self.ai_attack_time_zero_condition)
        c9 = Condition('AI공격쿨타임이 하나만 0인가', self.ai_one_attack_time_zero_condition)
        c10 = Condition('점수가 많음?', self.score_more_score_condition)
        c11 = Condition('일정거리 안으로 왔는가?', self.distance_less_than)
        c12= Condition('일정거리 밖에 있는가?', self.distance_more_than)
        c13= Condition('점수가 더 많은가?', self.score_more_score_condition)
        c14 = Condition('상대 공격 쿨타임이 0인가?', self.hero_attack_time_zero_condition)
        c15 = Condition('상대 공격 쿨타임이 0이 아닌가?', self.hero_attack_time_zero_not_condition)
        c16 = Condition('점수가 똑같은가?', self.score_equal_conditon)
        a1 = Action('앞으로가기', self.front_Move) #앞으로 이동
        a2 = Action('뒤로가기', self.back_Move)
        a3 = Action('방어하기', self.defence)
        a4 = Action('중단 공격하기', self.middle_attack)
        a5 = Action('상단 공격하기', self.up_attack)
        a6 = Action('IDLE', self.idle)
        ##
        SEQ_MIDDLE_ATTACK = Sequence('MIDDLE_ATTACK', c9, a4)
        SEL_UP_ATTACK_MIDDLE_ATTACK = Selector('UP_ATTACK_MIDDLE_ATTACK', SEQ_MIDDLE_ATTACK, a5)
        ##
        ##
        SEQ_TWO_ATTACK = Sequence('Two_Attack', c8, SEL_UP_ATTACK_MIDDLE_ATTACK)
        SEQ_DEFENCE = Sequence('DEFENCE', c7, a3)
        ##
        ##
        SEL_ATTACK_AND_DEFENCE = Selector('ATTACK_AND_DEFENCE', SEQ_DEFENCE, SEQ_TWO_ATTACK)
        ##
        ##
        SEQ_BEHAVIOR = Sequence('BEHAVIOR', c6, SEL_ATTACK_AND_DEFENCE)
        SEQ_BACK = Sequence('BACK', c5, a2)
        ##
        ##
        SEL_BEHAVIOR_AND_BACK = Selector('BEHAVIOR_AND_BACK', SEQ_BACK, SEQ_BEHAVIOR)
        ##
        #*
        SEQ_GO_MORE_SCORE = Sequence('GO_MORE_SCORE',c15,a1)
        SEQ_BACK_MORE_SCORE = Sequence('BACK_MORE_SCORE',c14,a2)
        #*
        ##
        SEQ_NOT_MEET = Sequence('NOT_MEET', c3, a1)
        SEQ_MEET = Sequence('MEET', c4, SEL_BEHAVIOR_AND_BACK)
        ##
        #*
        SEL_GO_AND_BACK = Selector('GO_AND_BACK', SEQ_GO_MORE_SCORE, SEQ_BACK_MORE_SCORE)
        SEQ_NOT_MEET_SCORE_MORE = Sequence('NOT_MEET_SCORE_MORE', c3, SEL_GO_AND_BACK)
        #*
        ##
        SEL_MEET_OR_NOT_MEET = Selector('MEET_OR_NOT_MEET',SEQ_NOT_MEET ,SEQ_MEET)
        SEQ_DISTANCE_LESS = Sequence('Distance_less', c11, SEL_MEET_OR_NOT_MEET)
        SEQ_DISTANCE_MORE = Sequence('Distance_more', c12, a1)
        ##
        #*
        SEL_MEET_OR_NOT_MEET_SCORE_MORE = Selector('MEET_OR_NOT_MEET_SCORE_MORE', SEQ_NOT_MEET_SCORE_MORE, SEQ_MEET)
        SEQ_DISTANCE_LESS_SCORE_MORE = Sequence('DISTANCE_MORE_SCORE_MORE', c11, SEL_MEET_OR_NOT_MEET_SCORE_MORE)
        #*
        ##
        SEL_DISTANCE_LESS_AND_MORE = Selector('DISTANCE_LESS_AND_MORE', SEQ_DISTANCE_LESS, SEQ_DISTANCE_MORE)
        SEQ_SCORE_LESS = Sequence('LESS_SCORE', c2, SEL_DISTANCE_LESS_AND_MORE)
        ##
        #*
        SEL_DISTANCE_LESS_AND_MORE_SCORE_MORE = Selector('DISTANCE_LESS_AND_MORE(SCORE_MORE)', SEQ_DISTANCE_LESS_SCORE_MORE, a6)
        SEQ_SCORE_MORE = Sequence('SCORE_MORE', c13, SEL_DISTANCE_LESS_AND_MORE_SCORE_MORE)
        #*

        #&
        SEQ_EQUAL = Sequence('EQUAL', c16, a5)
        SEQ_EQUAL = Sequence('EQUAL', c16, SEL_DISTANCE_LESS_AND_MORE)
        #&
        ##
        SEL_SCORE_MORE_AND_LESS = Selector('SCORE_MORE_AND_LESS', SEQ_SCORE_LESS, SEQ_SCORE_MORE)
        SEQ_NOT_EQUAL = Sequence('NOT_EQUAL', c1, SEL_SCORE_MORE_AND_LESS)
        ##
        root =  SEL_MIDDLE_SCORE_OR_NOT = Selector('MIDDLE_SCORE_OR_NOT', SEQ_NOT_EQUAL, SEQ_EQUAL)
        self.bt = BehaviorTree(root)
