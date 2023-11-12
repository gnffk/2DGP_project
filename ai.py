
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

from sdl2 import SDLK_a, SDL_Event, SDLK_s

import game_world
import game_framework

# state event check
# ( state event type, event value )

def attack_up(e):
    return e[0] == 'INPUT' and  e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def attack_middle(e):
    return e[0] == 'INPUT' and  e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def right(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def left(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT



def IDLE_return(e):
    return e[0] == 'NONE'


PIXEL_PER_METER= (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS* PIXEL_PER_METER)
# Boy Action Speed
# fill here
TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 11




class Idle:
    @staticmethod
    def enter(AI, e):
        AI.dir = 0
        AI.frame = 0
        AI.wait_time = get_time()
        print(e)
        pass

    @staticmethod
    def exit(AI, e):
        pass

    @staticmethod
    def do(AI):
        AI.frame = (AI.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                     * game_framework.frame_time) % 11

    @staticmethod
    def draw(AI):
        AI.image.clip_draw(int(AI.frame) * 500, 0 * 348, 500, 348, AI.x, AI.y)

class Attack_up:
    @staticmethod
    def enter(AI, e):
        AI.frame = 0
        print(e)
        pass

    @staticmethod
    def exit(AI, e):
        #print(hero.frame)
        pass

    @staticmethod
    def do(AI):
        AI.frame = (AI.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                     * game_framework.frame_time) % 11
        #print(hero.frame)
        if AI.frame >=10.9:
            print('end')
            AI.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(AI):
        print(int(AI.frame))
        AI.image_attack_up.clip_draw(int(AI.frame) * 500, 0 * 348, 500, 348,AI.x, AI.y)

class Attack_middle:
    @staticmethod
    def enter(AI, e):
        AI.frame = 0
        print(e)
        pass

    @staticmethod
    def exit(AI, e):
        print(AI.frame)
        pass

    @staticmethod
    def do(AI):
        AI.frame = (AI.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                     * game_framework.frame_time) % 11
        print(AI.frame)
        if AI.frame >=10.8:
            print('end')
            AI.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(AI):
        AI.image_attack_middle.clip_draw(int(AI.frame) * 500, 0 * 348, 500, 348, AI.x, AI.y)

class Run:
    @staticmethod
    def enter(AI, e):
        if right(e):
            AI.dir= 1
        elif left(e):
            AI.dir = -1

    @staticmethod
    def exit(AI, e):

        pass

    @staticmethod
    def do(AI):
        AI.frame = (AI.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                      * game_framework.frame_time) % 11
        AI.x += AI.dir * 0.5
        if AI.frame >=10.8:
            print('end')
            AI.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(AI):
        if AI.dir == 1:
            AI.image_run.clip_composite_draw(int(AI.frame) * 500, 0 * 348, 500, 348,AI.x, AI.y)
        elif AI.dir == -1:
            AI.image_run_back.clip_draw(int(AI.frame) * 500, 0 * 348, 500, 348, AI.x, AI.y)

class StateMachine:
    def __init__(self, AI):
        self.AI = AI
        self.cur_state = Idle
        self.transitions = {
            Idle: {right:Run,left:Run, attack_up: Attack_up,attack_middle: Attack_middle},
            Run:{IDLE_return:Idle},
            Attack_up: {IDLE_return:Idle},
            Attack_middle: {IDLE_return: Idle}
        }

    def start(self):
        self.cur_state.enter(self.AI, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.AI)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.AI, e)
                self.cur_state = next_state
                self.cur_state.enter(self.AI, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.AI)
class AI:
    def __init__(self):
        self.x, self.y = 1000, 150
        self.frame = 0
        self.action = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('Idle.png')
        self.image_attack_up = load_image('attack_up.png')
        self.image_attack_middle = load_image('attack_middle.png')
        self.image_run = load_image('run.png')
        self.image_run_back = load_image('run_back.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
