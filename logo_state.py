from pico2d import *
import game_framework
import play_state
import stage_state

back_ground_image = None
logo_image = None
press_start = None
logo_time = 0
logo_frame = 0
back_ground_x = 800//2
back_ground_y = 450//2
posX, posY = 800//2, 550//2
dir = 1
pdir = 1


def enter():
    global back_ground_image
    global logo_image
    global press_start
    back_ground_image = load_image('resource/logo_background.png')
    logo_image = load_image('resource/logo.png')
    press_start = load_image('resource/press_start.png')


def exit():
    global back_ground_image
    global logo_image
    global press_start
    del back_ground_image
    del logo_image
    del press_start


def update():
    global logo_time
    global logo_frame
    global back_ground_x
    global press_start
    global dir
    global pdir
    global posY
    logo_frame = (logo_frame + 10 * game_framework.frame_time) % 40

    if back_ground_x > 450 or back_ground_x < 350:
        dir *= -1
    back_ground_x += 10 * dir * game_framework.frame_time

    if posY > 285 or posY < 275:
        pdir *= -1
    posY += 10 * pdir * game_framework.frame_time


def draw():
    global back_ground_image
    global logo_image
    clear_canvas()
    back_ground_image.draw(back_ground_x, back_ground_y, 900, 450)
    logo_image.clip_composite_draw(int(logo_frame) * 189, 0,
                                   189, 124, 0, ' ', posX, posY, 500, 327)
    press_start.draw(400, 68, 800, 136)

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
