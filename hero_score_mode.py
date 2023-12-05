from pico2d import *

import game_framework
import game_world
import play_mode
import server

from pannel import Pannel


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_0:

                    game_framework.pop_mode()
                case pico2d.SDLK_1:

                    game_framework.pop_mode()
                case pico2d.SDLK_2:

                    game_framework.pop_mode()


def init():
    global pannel
    global score_mode_start_time
    server.pannel = Pannel()
    game_world.add_object(server.pannel, 3)

    score_mode_start_time = get_time()
def update():
    global score_mode_start_time
    if get_time() - score_mode_start_time >= 3.0:
        score_mode_start_time = get_time()
        game_framework.pop_mode()
    game_world.update()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.remove_object(server.pannel)
    pass

def pause():
    pass
def resume():
    pass