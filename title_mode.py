from pico2d import *
import game_framework
import play_mode
def init():
     global image
     image = load_image('resource/title.png')
def update():
    pass
def finish():
     global image
     del image
def handle_events():
     events = get_events()
     for event in events:
         if event.type == SDL_QUIT:
            game_framework.quit()
         elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)
def draw():
     clear_canvas()
     image.clip_draw(0, 0 , get_canvas_width(), get_canvas_height(), 800, 400)
     update_canvas()
