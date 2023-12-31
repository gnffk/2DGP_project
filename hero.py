from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, draw_rectangle, \
    load_music

from score import Score
from sdl2 import SDLK_a, SDL_Event, SDLK_s, SDLK_d

import game_world
import game_framework
import server


# state event check
# ( state event type, event value )

def attack_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def attack_middle(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def right(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def left(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def defence(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def IDLE_return(e):
    return e[0] == 'NONE'


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
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
        # print(e)
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
        hero.image.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y, 500, 348)


class Attack_up:
    @staticmethod
    def enter(hero, e):
        hero.frame = 0
        hero.bgm_attack.play(1)
        # (e)
        pass

    @staticmethod
    def exit(hero, e):
        # print(hero.frame)
        pass

    @staticmethod
    def do(hero):
        if hero.attack_up_cooldown == 0:
            hero.state = 'ATTACK'
            hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                          * game_framework.frame_time) % 11
            if server.score.score_state_hero == False:
                if hero.frame <= 5.5:
                    hero.weapon_x += RUN_SPEED_PPS * game_framework.frame_time / 2
                elif hero.frame > 5.5:
                    hero.weapon_x -= RUN_SPEED_PPS * game_framework.frame_time / 2
                # print(hero.frame)
            if hero.frame >= 10.9:
                hero.attack_up_cooldown = 5
                print('end')
                hero.state = 'IDLE'
                hero.state_machine.handle_event(('NONE', 0))
        else:
            hero.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(hero):
        # print(int(hero.frame))
        hero.image_attack_up.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y, 500,
                                                 348)


class Attack_middle:
    @staticmethod
    def enter(hero, e):
        hero.frame = 0
        hero.bgm_attack.play(1)
        # print(e)
        pass

    @staticmethod
    def exit(hero, e):
        # print(hero.frame)
        pass

    @staticmethod
    def do(hero):
        if hero.attack_middle_cooldown == 0:
            hero.state = 'Attack'
            hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                          * game_framework.frame_time) % 11

            if server.score.score_state_hero == False:
                if hero.frame <= 5.5:
                    hero.weapon_x += RUN_SPEED_PPS * game_framework.frame_time / 2
                elif hero.frame > 5.5:
                    hero.weapon_x -= RUN_SPEED_PPS * game_framework.frame_time / 2
            # print(hero.frame)
            if hero.frame >= 10.8:
                hero.attack_middle_cooldown = 5
                print('end')
                hero.state = 'IDLE'
                hero.state_machine.handle_event(('NONE', 0))
            pass
        else:
            hero.state_machine.handle_event(('NONE', 0))

    @staticmethod
    def draw(hero):
        hero.image_attack_middle.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y,
                                                     500, 348)


class Defence:
    @staticmethod
    def enter(hero, e):
        hero.frame = 0

        # print(e)
        pass

    @staticmethod
    def exit(hero, e):
        print(hero.frame)
        pass

    @staticmethod
    def do(hero):
        if hero.defence_cooldown == 0:
            hero.state = 'defence'
            hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                          * game_framework.frame_time) % 11

            if hero.frame >= 10.8:
                hero.defence_cooldown = 5
                print('end')
                hero.state = 'IDLE'
                hero.state_machine.handle_event(('NONE', 0))
        else:
            hero.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(hero):
        hero.image_defence.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y, 500,
                                               348)


class Run:
    @staticmethod
    def enter(hero, e):
        if right(e) and not left(e):
            hero.dir = 1
        elif left(e) and not right(e):
            hero.dir = -1

    @staticmethod
    def exit(hero, e):
        pass

    @staticmethod
    def do(hero):
        hero.frame = (hero.frame + FRAMES_PER_ACTION * ACTION_PER_TIME
                      * game_framework.frame_time) % 11
        hero.x += hero.dir * RUN_SPEED_PPS * game_framework.frame_time
        hero.weapon_x = hero.x +100
        if hero.frame >= 10.8:
            print('end')
            hero.state_machine.handle_event(('NONE', 0))
        pass

    @staticmethod
    def draw(hero):
        if hero.dir == 1:
            hero.image_run.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y, 500,
                                               348)
        elif hero.dir == -1:
            hero.image_run_back.clip_composite_draw(int(hero.frame) * 500, 0 * 348, 500, 348, 0, 'h', hero.x, hero.y,
                                                    500, 348)


class StateMachine:
    def __init__(self, hero):
        self.hero = hero
        self.cur_state = Idle
        self.transitions = {
            Idle: {right: Run, left: Run, attack_up: Attack_up, attack_middle: Attack_middle, defence: Defence},
            Run: {IDLE_return: Idle},
            Attack_up: {IDLE_return: Idle},
            Attack_middle: {IDLE_return: Idle},
            Defence: {IDLE_return: Idle}
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
        self.weapon_x, self.weapon_y = 700, 230
        self.frame = 0
        self.action = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('resource/Idle.png')
        self.image_attack_up = load_image('resource/attack_up.png')
        self.image_attack_middle = load_image('resource/attack_middle.png')
        self.image_run = load_image('resource/run.png')
        self.image_run_back = load_image('resource/run_back.png')
        self.image_defence = load_image('resource/defence.png')
        self.image_a = load_image('resource/cooldown/A_cooldown.png')
        self.image_s = load_image('resource/cooldown/S_cooldown.png')
        self.image_d = load_image('resource/cooldown/D_cooldown.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.count = 0
        self.attack_up_cooldown = 0
        self.attack_middle_cooldown = 0
        self.defence_cooldown = 0
        self.state = 'IDLE'
        self.bgm_hit = load_music('resource/music/hit.mp3')
        self.bgm_hit.set_volume(50)
        self.bgm_attack = load_music('resource/music/attack.mp3')
        self.bgm_attack.set_volume(50)

        self.bgm_score = load_music('resource/music/score_up.mp3')
        self.bgm_score.set_volume(50)
    def handle_event(self, event):
        # print(event)
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        if self.attack_up_cooldown > 0:
            self.attack_up_cooldown -= game_framework.frame_time
            if self.attack_up_cooldown < 0:
                self.attack_up_cooldown = 0
        if self.attack_middle_cooldown > 0:
            self.attack_middle_cooldown -= game_framework.frame_time
            if self.attack_middle_cooldown < 0:
                self.attack_middle_cooldown = 0
        if self.defence_cooldown > 0:
            self.defence_cooldown -= game_framework.frame_time
            if self.defence_cooldown < 0:
                self.defence_cooldown = 0


        self.state_machine.update()

    def draw(self):
        self.image_a.clip_draw(int(self.attack_up_cooldown) * 150, 0, 150, 150, 120,700,70,70)
        self.image_s.clip_draw(int(self.attack_middle_cooldown)*150, 0, 150, 150, 200, 700,70,70)
        self.image_d.clip_draw(int(self.defence_cooldown) * 150, 0, 150, 150, 280,700 ,70,70)


        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_aa())
        # print(server.ai.x - self.x)
        if server.ai.x - self.x < 100:
            self.x = server.ai.x - 100
            self.weapon_x = self.x + 100
            self.weapon_y = self.y + 80

    def get_bb(self):
        return self.x - 120, self.y - 100, self.x - 30, self.y + 90

    def get_aa(self):
        return self.weapon_x, self.weapon_y, self.weapon_x + 14, self.weapon_y + 14

    def handle_collision(self, group, other):
        if group == 'hero:ai':
            if server.ai.state != 'defence':  # defence 일때는 공격 추가 안됨
                self.bgm_score.play(1)
                server.score.score_state_hero = True
                server.score.hero_score += 1
                self.x = server.ai.x - 100
                self.weapon_x = server.ai.x
            # print("찌름")
            pass
