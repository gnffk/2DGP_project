
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
    def enter(hero, e):
        hero.dir = 0
        hero.frame = 0
        hero.wait_time = get_time()
        print(e)
        pass

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                     * game_framework.frame_time) % 11

    @staticmethod
    def draw(hero):
        hero.image.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y,500,348)

class Attack_up:
    @staticmethod
    def enter(hero, e):
        hero.frame = 0
        print(e)
        pass

    @staticmethod
    def exit(hero, e):
        #print(hero.frame)
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                     * game_framework.frame_time) % 11
        #print(hero.frame)
        if hero.frame >=10.9:
            print('end')
            hero.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(hero):
        print(int(hero.frame))
        hero.image_attack_up.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y,500,348)

class Attack_middle:
    @staticmethod
    def enter(hero, e):
        hero.frame = 0
        print(e)
        pass

    @staticmethod
    def exit(hero, e):
        print(hero.frame)
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                     * game_framework.frame_time) % 11
        print(hero.frame)
        if hero.frame >=10.8:
            print('end')
            hero.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.image_attack_middle.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y,500,348)

class Run:
    @staticmethod
    def enter(hero, e):
        if right(e):
            hero.dir= 1
        elif left(e):
            hero.dir = -1

    @staticmethod
    def exit(hero, e):

        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                      * game_framework.frame_time) % 11
        hero.x += hero.dir * 0.5
        if hero.frame >=10.8:
            print('end')
            hero.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(hero):
        if hero.dir == 1:
            hero.image_run.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y,500,348)
        elif hero.dir == -1:
            hero.image_run_back.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y,500,348)

class StateMachine:
    def __init__(self, hero):
        self.hero = hero
        self.cur_state = Idle
        self.transitions = {
            Idle: {right:Run,left:Run, attack_up: Attack_up,attack_middle: Attack_middle},
            Run:{IDLE_return:Idle},
            Attack_up: {IDLE_return:Idle},
            Attack_middle: {IDLE_return: Idle}
        }

    def start(self):
        self.cur_state.enter(self.hero, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.hero)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hero, e)
                self.cur_state = next_state
                self.cur_state.enter(self.hero, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.hero)
class Hero:
    def __init__(self):
        self.x, self.y = 600, 150
        self.frame = 0
        self.action = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('resource/Idle.png')
        self.image_attack_up = load_image('resource/attack_up.png')
        self.image_attack_middle = load_image('resource/attack_middle.png')
        self.image_run = load_image('resource/run.png')
        self.image_run_back = load_image('resource/run_back.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
