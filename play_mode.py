from pico2d import *

import game_framework
import game_world
import hero_score_mode
from hero import Hero
from ai import AI
from score import Score

from background import FixedBackground as Background
import server
# Game object class here
import title_mode
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            server.hero.handle_event(event)
            pass


def init():
    global running
    global hero,ai,score
    running = True

    server.score = Score()
    game_world.add_object(server.score, 1)

    server.background = Background()
    game_world.add_object(server.background, 0)

    server.hero = Hero()
    game_world.add_object(server.hero, 1)


    server.ai = AI()
    game_world.add_object(server.ai, 1)

    game_world.add_collision_pair('ai:hero', server.ai, None)
    game_world.add_collision_pair('ai:hero', None, server.hero)

    game_world.add_collision_pair('hero:ai', server.hero, None)
    game_world.add_collision_pair('hero:ai', None, server.ai)

def update():
    if server.score.score_state_hero == True or server.score.score_state_ai == True:
        game_framework.push_mode(hero_score_mode)
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

    pass
def resume():
    pass