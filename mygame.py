import game_framework
import pico2d
import logo_state
import play_state

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450

pico2d.open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
game_framework.run(play_state)
pico2d.close_canvas() 