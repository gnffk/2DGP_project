from pico2d import *

import game_framework
import game_world
from hero import Hero


# Game object class here

def handle_events():
    global running
    global attack_up
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            pass
        else:
            boy.handle_event(event)


def init():
    global running
    global hero
    running = True

    hero = Hero()
    game_world.add_object(hero, 1)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass

def pause():
    hero.wait_time = 10000000000000000000000000000000000000000000.0

    pass
def resume():
    hero.wait_time = get_time()
    pass