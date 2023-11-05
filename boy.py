from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from sdl2 import SDLK_a, SDL_Event

import game_world

# state event check
# ( state event type, event value )

def attack_up(e):
    return e[0] == 'INPUT' and  e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def attack_up_return(e):
    return e[0] == 'INPUT' and  e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def IDLE_return(e):
    return e[0] == 'NONE'

class Idle:
    @staticmethod
    def enter(boy, e):
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()
        print(e)
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 11

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 500, 0 * 348, 500, 348, boy.x, boy.y)

class Attack_up:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        print(e)
        pass

    @staticmethod
    def exit(boy, e):
        print(boy.frame)
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 11
        if boy.frame == 0:
            print('end')
            boy.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image_attack_up.clip_draw(boy.frame * 500, 0 * 348, 500, 348, boy.x, boy.y)



class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir, boy.action, boy.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action, boy.face_dir = -1, 0, -1

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 11
        boy.x += boy.dir * 5
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle, attack_up: Attack_up},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
            Attack_up: {IDLE_return:Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.boy)
class Boy:
    def __init__(self):
        self.x, self.y = 600, 150
        self.frame = 0
        self.action = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('Idle.png')
        self.image_attack_up = load_image('attack_up.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
