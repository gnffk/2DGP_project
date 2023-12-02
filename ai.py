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
        self.build_behavior_tree()

    def get_bb(self):
        return self.x+30 , self.y-100, self.x + 120 , self.y + 90 #충돌 박스 크기 x = 90 / y = 190

    def get_aa(self):
        return self.weapon_x, self.weapon_y, self.weapon_x+ 14, self.weapon_y + 14

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()

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

    def build_behavior_tree(self):
        #a1 = Action('Set random location', self.set_random_location)
        #a2 = Action('Move to', self.move_to)
        #root = SEQ_wander = Sequence('Wander', a1, a2)
        a1 = Action('앞으로가기', self.go_to)
        c1 = Condition('만났냐?', self.meet_condition)
        a2 = Action('뒤로가기', self.back_go_to)
        c2 = Condition('AI 방어 쿨타임이 없어?', self.defence_action)
        a3 = Action('방어하기', self.defence)
        c3 = Condition('상대방이 공격중이야?', self.hero_attack_condition)
        c4 = Condition('나의 공격 쿨타임이 하나라도 0인가?', self.ai_two_attack_condition)
        c5 = Condition('미들공격 쿨타임 = 0, 상단공격 쿨타임이 != 0 인가?', self.middle_attack_condition)
        a4 = Action('중간 공격', self.middle_attack)
        c6 = Condition('미들공격 쿨타임 = 0, 상단공격 쿨타임이 = 0 인가?', self.high_attack_condition)
        a5 = Action('상단 공격', self.high_attack)
        #제일 왼쪽부터


        SEQ_TO_GO= Sequence('앞으로 이동', c1, a1)
        SEQ_BACK_GO_TO = Sequence('뒤로 이동', c2, a2)
        SEQ_DEFENCE = Sequence('방어', c3, a3)
        SEQ_ATTACK_MIDDLE = Sequence('중단 공격', c5, a4)
        SEQ_ATTACK_HIGH = Sequence('상단공격', c6, a5)
        SEL_HIGH_MIDDLE_ATTACK = Selector('HIGH_MIDDLE_ATTACK', SEQ_ATTACK_MIDDLE, SEQ_ATTACK_HIGH)
        SEQ_TWO_ATTACK_MOTION = Sequence('공격2개', c4, SEL_HIGH_MIDDLE_ATTACK)
        SEL_ATTACK_AND_DEFENCE = Selector('ATTACK_DEFENCE',  SEQ_DEFENCE, SEQ_TWO_ATTACK_MOTION)
        SEL_BEHAVIOR_ATTACK_AND_DEFENCE = Selector('ATTACK_AND_DEFENCE',SEQ_BACK_GO_TO, SEL_ATTACK_AND_DEFENCE )
        SEL_MEET_OR_NOT = Selector('MEET_OR_NOT', SEQ_TO_GO, SEL_BEHAVIOR_ATTACK_AND_DEFENCE)
        SEL_DISTANCE_CLOSE_AND_FAR = Selector('DISTANCE_CLOSE_AND_FAR', SEL_MEET_OR_NOT, SEQ_TO_GO)


        SEL_SCORE_EQUAL = Selector('SCORE_EQUAL',SEL_LOW_AND_HIGH, SEL_DISTANCE_CLOSE_AND_FAR)
        self.bt = BehaviorTree(root)
