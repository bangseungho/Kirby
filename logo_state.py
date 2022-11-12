from pico2d import *
import game_framework
import play_state
import stage_state

image = None


def enter():
    global image
    image = load_image('presource/logo.png')


def exit():
    global image
    del image


def update():
    global logo_time
    delay(0.01)

def draw():
    global image
    clear_canvas()
    image.draw(800//2, 450//2)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(stage_state)
