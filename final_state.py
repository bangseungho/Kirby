from pico2d import *
import game_framework
import server
import datetime

back_ground_image = None
back_ground_die_image = None
logo_time = 0
logo_frame = 0
back_ground_x = 800//2
back_ground_y = 450//2
posX, posY = 800//2, 550//2
dir = 1
pdir = 1
bgm = None

def enter():
    from kirby import IDLE
    global back_ground_image
    global back_ground_die_image
    back_ground_image = load_image('resource/black.png')
    back_ground_die_image = load_image('resource/black_die.png')
    server.clear_time = datetime.datetime.now()
    server.elapsed = server.clear_time - server.start_time
    server.player.cur_state = IDLE

def exit():
    pass


def update():
    import play_state
    global logo_time
    global logo_frame
    global back_ground_x
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
    play_state.update()


def draw():
    import play_state
    global back_ground_image
    global back_ground_die_image
    clear_canvas()
    play_state.draw_world()
    font = load_font('ChubbyChoo.TTF', 16)
    if  server.player_die == False:
        back_ground_image.draw(back_ground_x, back_ground_y, 1000, 600)
        font.draw(300, 265, f'PLAY TIME - {server.elapsed.seconds} : {server.elapsed.microseconds}', (255, 255, 255))
        font.draw(300, 225, 'THANKS FOR YOUR PLAY', (255, 155, 0))
        font.draw(300, 185, 'MADE BY SEUNGHO BAEK', (255, 155, 0))
    elif server.player_die:
        back_ground_die_image.draw(back_ground_x, back_ground_y, 1000, 600)
        font.draw(355, 250, 'YOU ARE DIED', (255, 255, 255))
        font.draw(300, 200, 'PRESS THE ESCAPE TO QUIT', (255, 155, 0))
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
