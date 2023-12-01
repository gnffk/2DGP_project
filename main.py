import pico2d
from pico2d import open_canvas, close_canvas,delay
import game_framework
#import logo_mode as start_mode
#import title_mode as start_mode
import play_mode as start_mode
#import item_mode as start_mode


open_canvas(1600,800)
game_framework.run(start_mode)
close_canvas()

