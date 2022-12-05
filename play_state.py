from pico2d import *
import game_framework
import game_world

import server

from kirby import Kirby
from stage_1 import Stage
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
    KBeam_Laser = 9
    Dedede = 10
    Dstar = 11

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
            pass
            server.player.handle_event(event)
            server.stage.handle_event(event)

# 초기화
def enter():
    server.stage = Stage()
    game_world.add_object(server.stage, 0)

    server.player = Kirby()
    game_world.add_object(server.player, 1)

    # 충돌 대상 정보 등록
    game_world.add_collision_pairs(server.player, server.enemy, 'player:enemy')
    game_world.add_collision_pairs(server.player, server.stage.obstacles, 'player:ob')
    game_world.add_collision_pairs(None, server.player, 'beams:player')
    game_world.add_collision_pairs(None, server.player, 'fire:player')

    game_world.add_collision_pairs(None, server.enemy, 'star:enemy')
    game_world.add_collision_pairs(None, server.enemy, 'kbeam:enemy')
    game_world.add_collision_pairs(None, server.stage.obstacles, 'star:ob')
    game_world.add_collision_pairs(server.stage.obstacles, server.enemy, 'enemy:ob')
    pass

# 종료
def exit():
    game_world.clear()
    
def update():
    for game_object in game_world.all_objects():
        game_object.update()
        game_object.isCollide = False

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
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
