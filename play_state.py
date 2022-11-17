from pico2d import *
import game_framework
import stage_state
import logo_state
import kirby
import game_world
from kirby import Kirby
from stage_1 import Stage
from spark import Spark
from star import Star
from hothead import Fire
from enum import Enum

class Type(Enum):
    Stage = 0
    Kirby = 1
    Spark = 2
    Laser = 3
    Hothead = 4
    Star = 5
    Breath = 6
    Fire = 7
    Beam_Laser = 8



stage = None
star = None

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
            stage.player.handle_event(event)
            stage.move_stage(event, stage.player.x, stage.player.y)

# 초기화
def enter():
    global stage
    global star
    # global enemys
    stage = Stage()
    star = Star()
    game_world.add_object(stage, 0)
    game_world.add_object(star, 1)

    # 충돌 대상 정보 등록
    game_world.add_collision_pairs(star, stage.enemys, 'star:enemy')
    game_world.add_collision_pairs(star, stage.obstacles, 'star:ob')
    game_world.add_collision_pairs(stage.obstacles, stage.enemys, 'enemy:ob')
# 종료
def exit():
    game_world.clear()
    
def update():
    for game_object in game_world.all_objects():
        game_object.update()
        game_object.isCollide = False

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            # if type(a) != Kirby:
            #     print(group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)


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

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False
    return True

def test_self():
    import play_state
    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
