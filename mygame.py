import game_framework
import pico2d
import logo_state
from ResourceMgr import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

pico2d.open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)  
ResourceMgr().Load()
game_framework.run(logo_state)
pico2d.close_canvas()