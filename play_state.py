from pico2d import *
import game_framework
import stage_state
import logo_state
import game_world
from kirby import Kirby
from stage_1 import Stage

player = None
stage = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            if len(game_framework.stack) == 2:
                game_framework.pop_state()
            else:
                game_framework.quit()
        else:
            player.handle_event(event)
            stage.move_stage(event, player.x, player.y)

# 초기화
def enter():
    global player
    global stage
    player = Kirby()
    stage = Stage()
    game_world.add_object(player, 1)
    game_world.add_object(stage, 0)

# 종료
def exit():
    game_world.clear()
    
def update():
    for game_object in game_world.all_objects():
        game_object.update()

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def test_self():
    import play_state
    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
