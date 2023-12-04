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
        self.x = 950
        self.y = 150
        self.weapon_x, self.weapon_y = 830, 230
        self.size_x = 500
        self.size_y = 348
        self.load_images()
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = 0
        self.state = 'Idle'

        self.tx, self.ty = 0, 0
        # self.build_behavior_tree()

    def get_bb(self):
        return self.x+30 , self.y-100, self.x + 120 , self.y + 90 #충돌 박스 크기 x = 90 / y = 190

    def get_aa(self):
        return self.weapon_x, self.weapon_y, self.weapon_x+ 14, self.weapon_y + 14

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # self.bt.run()

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        image = AI.images[self.state][0]  # 가져온 이미지 리스트에서 첫 번째 이미지를 사용

        image.clip_draw(int(self.frame) * 500, 0 * 348, 500, 348, sx, sy)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_aa())
        if self.x- server.hero.x<100:
            self.x = server.hero.x+100
            self.weapon_x= self.x -120

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):

        pass

    def move_to(self, r=0.5):
        self.state = 'Idle'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        # select random location around boy
        self.tx = 1000
        self.ty = -200
        return BehaviorTree.SUCCESS

    def handle_collision(self, group, other):
        if group == 'ai:hero':


            print("찌름")
            pass

    # def build_behavior_tree(self):
    #     #a1 = Action('Set random location', self.set_random_location)
    #     #a2 = Action('Move to', self.move_to)
    #     #root = SEQ_wander = Sequence('Wander', a1, a2)
    #     c1 = Condition('점수가 안똑같음?', self.score_not_equal_condition)
    #     c2 = Condition('점수가 적음?', self.score_less_score_condition)
    #     c3 = Condition('못만남?', self.score_not_meet_condition)
    #     c4 = Condition('만남?',self.score_meet_condition )
    #     c5 = Condition('방어 쿨타임 0이상인가?',self.ai_defecne_time_up_condition)
    #     c6 = Condition('방어 쿨타임이 0인가',self.ai_defecne_time_zero_condition)
    #     c7 = Condition('상대방이 공격중인가?', self.hero_attack_condition)
    #     c8 = Condition('둘중에 하나라도 AI 공격쿨타임이 0인가?', self.ai_attack_time_zero_condition)
    #     c9 = Condition('AI공격쿨타임이 하나만 0인가', self.ai_one_attack_time_zero_condition)
    #     c10 = Condition('점수가 많음?', self.score_more_score_condition)
    #     c11 = Condition('일정거리 안으로 왔는가?', self.distance_less_than)
    #     c12= Condition('일정거리 밖에 있는가?', self.distance_more_than)
    #     c13= Condition('점수가 더 많은가?', self.score_more_score_condition)
    #     c14 = Condition('상대 공격 쿨타임이 0인가?', self.hero_attack_time_zero_condition)
    #     c15 = Condition('상대 공격 쿨타임이 0이 아닌가?', self.hero_attack_time_zero_not_condition)
    #     c16 = Condition('점수가 똑같은가?', self.score_equal_conditon)
    #
    #     a1 = Action('앞으로가기', self.front_Move) #앞으로 이동
    #     a2 = Action('뒤로가기', self.back_Move)
    #     a3 = Action('방어하기', self.defence)
    #     a4 = Action('중단 공격하기', self.middle_attack)
    #     a5 = Action('상단 공격하기', self.up_attack)
    #     a6 = Action('IDLE', self.idle)
    #
    #
    #     ##
    #     SEQ_MIDDLE_ATTACK = Sequence('MIDDLE_ATTACK', c9, a4)
    #     SEL_UP_ATTACK_MIDDLE_ATTACK = Selector('UP_ATTACK_MIDDLE_ATTACK', SEQ_MIDDLE_ATTACK, a5)
    #     ##
    #
    #     ##
    #     SEQ_TWO_ATTACK = Sequence('Two_Attack', c8, SEL_UP_ATTACK_MIDDLE_ATTACK)
    #     SEQ_DEFENCE = Sequence('DEFENCE', c7, a3)
    #     ##
    #
    #     ##
    #     SEL_ATTACK_AND_DEFENCE = Selector('ATTACK_AND_DEFENCE', SEQ_DEFENCE, SEQ_TWO_ATTACK)
    #     ##
    #
    #     ##
    #     SEQ_BEHAVIOR = Sequence('BEHAVIOR', c6, SEL_ATTACK_AND_DEFENCE)
    #     SEQ_BACK = Sequence('BACK', c5, a2)
    #     ##
    #
    #     ##
    #     SEL_BEHAVIOR_AND_BACK = Selector('BEHAVIOR_AND_BACK', SEQ_BACK, SEQ_BEHAVIOR)
    #     ##
    #     #*
    #     SEQ_GO_MORE_SCORE = Sequence('GO_MORE_SCORE',c15,a1)
    #     SEQ_BACK_MORE_SCORE = Sequence('BACK_MORE_SCORE',c14,a2)
    #     #*
    #     ##
    #     SEQ_NOT_MEET = Sequence('NOT_MEET', c3, a1)
    #     SEQ_MEET = Sequence('MEET', c4, SEL_BEHAVIOR_AND_BACK)
    #     ##
    #
    #     #*
    #     SEL_GO_AND_BACK = Selector('GO_AND_BACK', SEQ_GO_MORE_SCORE, SEQ_BACK_MORE_SCORE)
    #     SEQ_NOT_MEET_SCORE_MORE = Sequence('NOT_MEET_SCORE_MORE', c3, SEL_GO_AND_BACK)
    #     #*
    #
    #     ##
    #     SEL_MEET_OR_NOT_MEET = Selector('MEET_OR_NOT_MEET',SEQ_NOT_MEET ,SEQ_MEET)
    #     SEQ_DISTANCE_LESS = Sequence('Distance_less', c11, SEL_MEET_OR_NOT_MEET)
    #     SEQ_DISTANCE_MORE = Sequence('Distance_more', c12, a1)
    #     ##
    #
    #     #*
    #     SEL_MEET_OR_NOT_MEET_SCORE_MORE = Selector('MEET_OR_NOT_MEET_SCORE_MORE', SEQ_NOT_MEET_SCORE_MORE, SEQ_MEET)
    #     SEQ_DISTANCE_LESS_SCORE_MORE = Sequence('DISTANCE_MORE_SCORE_MORE', c11, SEL_MEET_OR_NOT_MEET_SCORE_MORE)
    #     #*
    #
    #     ##
    #     SEL_DISTANCE_LESS_AND_MORE = Selector('DISTANCE_LESS_AND_MORE', SEQ_DISTANCE_LESS, SEQ_DISTANCE_MORE)
    #     SEQ_SCORE_LESS = Sequence('LESS_SCORE', c2, SEL_DISTANCE_LESS_AND_MORE)
    #     ##
    #
    #     #*
    #     SEL_DISTANCE_LESS_AND_MORE_SCORE_MORE = ('DISTANCE_LESS_AND_MORE(SCORE_MORE)', SEQ_DISTANCE_LESS_SCORE_MORE, a6)
    #     SEQ_SCORE_MORE = Sequence('SCORE_MORE', c13, SEL_DISTANCE_LESS_AND_MORE_SCORE_MORE)
    #     #*
    #
    #     #&
    #     SEQ_EQUAL = Sequence('EQUAL', c16, SEL_DISTANCE_LESS_AND_MORE)
    #     #&
    #     ##
    #     SEL_SCORE_MORE_AND_LESS = Selector('SCORE_MORE_AND_LESS', SEQ_SCORE_LESS, SEQ_SCORE_MORE)
    #     SEQ_NOT_EQUAL = Sequence('NOT_EQUAL', c1, SEL_SCORE_MORE_AND_LESS)
    #     ##
    #     root =  SEL_MIDDLE_SCORE_OR_NOT = Selector('MIDDLE_SCORE_OR_NOT', SEQ_NOT_EQUAL, SEQ_EQUAL)
    #     self.bt = BehaviorTree(root)
