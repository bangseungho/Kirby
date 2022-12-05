from pico2d import *
import game_framework
import play_state
import logo_state

image = None
bgm = None

def enter():
    global image
    global bgm
    image = load_image('resource/stage.png')
    bgm = load_music('sound/Stage.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()
    pass


def exit():
    global image
    del image
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(logo_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.push_state(play_state)


def draw():
    clear_canvas()
    image.draw(800//2, 450//2, 800, 450)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
