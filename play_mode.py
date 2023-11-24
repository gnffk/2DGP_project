from pico2d import *

import Win_mood
import game_framework
import game_world
import hero_score_mode
import Lose_mood
from hero import Hero
from ai import AI
from score import Score
from background import FixedBackground as Background
import server


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_0:
                server.score.ai_score = 10
            elif event.key == SDLK_1:
                server.score.hero_score = 10
            elif event.key == SDLK_2:
                server.score.real_score_hero = 2
                server.score.real_score_ai = 2
            else:
                server.hero.handle_event(event)


def init():
    global hero, ai, score, background
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
    global turn
    if server.score.score_state_hero or server.score.score_state_ai:
        game_framework.push_mode(hero_score_mode)

    if server.score.real_score_ai == 3:
        game_framework.change_mode(Lose_mood)

    if server.score.real_score_hero == 3:
        game_framework.change_mode(Win_mood)

    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()


def pause():
    pass


def resume():
    pass
