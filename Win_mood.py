from pico2d import *
import game_framework
import game_world
import play_mode
import server
import title_mode


def init():
    global image, alpha
    image = load_image('resource/mood/002.png')
    alpha = 0.0  # 초기 투명도

def update():
    global alpha
    alpha += 0.001  # 적절한 값으로 조절
    if alpha > 1.0:
        alpha = 1.0

def finish():
    global image
    server.hero = None
    server.ai = None
    game_world.clear()
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_r:

                game_framework.change_mode(title_mode)
                pass


def draw():
    clear_canvas()
    image.opacify(alpha)  # 투명도 적용
    image.clip_draw(0, 0, get_canvas_width(), get_canvas_height(), 800, 400)
    update_canvas()
