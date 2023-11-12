from pico2d import *

import game_framework
import game_world
from hero import Hero
from ai import AI
from score import Score

# Game object class here

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            pass
        else:
            hero.handle_event(event)


def init():
    global running
    global hero,ai,score
    running = True

    score = Score()
    game_world.add_object(score, 0)

    hero = Hero()
    game_world.add_object(hero, 1)


    ai = AI()
    game_world.add_object(ai, 1)

    game_world.add_collision_pair('ai:hero', ai, None)
    game_world.add_collision_pair('ai:hero', None, hero)

    game_world.add_collision_pair('hero:ai', hero, None)
    game_world.add_collision_pair('hero:ai', None, ai)

def update():
    game_world.update()
    game_world.handle_collisions()
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