from pico2d import *
import game_world
import game_framework
from player_speed import *
from spark import Spark
from laser import Laser
from hothead import Hothead
import server

NEXT, PREV, UD = range(3)

event_name = ['NEXT', 'PREV', 'UD']

cnt = 0

class Obstacle:
    def __init__(self, x, y, w, h):
        self.px, self.py = x, y
        self.x, self.y = x, y
        self.sx, self.sy = x, y
        self.w, self.h = w, h

    def get_bb(self):
        return self.x - self.w, self.y - self.h, self.x + self.w, self.y + self.h
    
    def handle_collision(self, other, group):
        if group == 'star:ob':
            pass
        pass


class STAGE_1:
    @staticmethod
    def enter(self, event):
        self.background_image = load_image('resource/stage1_background.png')
        self.land_image = load_image('resource/stage1_land.png')

        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.land_image.w
        self.h = self.land_image.h

        self.add_obstacle(800, 38, 800, 30)
        self.add_obstacle(2010, 200, 10, 100)
        self.add_obstacle(582.5, 85, 24, 15)
        self.add_obstacle(1157.5, 85, 89, 15)
        self.add_obstacle(1695, 85, 303, 15)
        self.add_obstacle(1605, 165, 30, 65)
        self.add_obstacle(1647.5, 132, 14, 35)
        self.add_enemy(1, Spark)
        self.add_enemy(1, Laser)
        self.add_enemy(1, Hothead)
        game_world.add_objects(server.enemy, 1)
        print('ENTER STAGE1')

    @staticmethod
    def exit(self, event):
        print('EXIT STAGE1')

    @staticmethod
    def do(self):
        self.window_left = clamp(
            0, int(server.player.x) - self.canvas_width//2, self.w - self.canvas_width - 1)
        self.window_bottom = clamp(
            0, int(server.player.y) - self.canvas_height//2, self.h - self.canvas_height-1)

    @staticmethod
    def draw(self):
        for ob in self.obstacles:
            ob.x = ob.sx - self.window_left
            ob.y = ob.sy - self.window_bottom

        self.sx, self.sy = self.canvas_width//2 - self.window_left / 10, self.canvas_height//2 - self.window_bottom

        self.background_image.draw(self.sx, self.sy, 1125, 500)

        self.land_image.clip_draw_to_origin(
            self.window_left, self.window_bottom, self.canvas_width, self.canvas_height, 0, 0,
            self.canvas_width, self.canvas_height / 1.5
        )


# class STAGE_2:
#     @staticmethod
#     def enter(self, event):
#         self.background_image = load_image('resource/stage2_background.png')
#         self.land_image = load_image('resource/stage2_land.png')
#         self.next_portal = [600, 90, 650, 140]
#         self.prev_portal = [0, 0, 0, 0]
#         self.add_obstacle(800, 38, 800, 30)
#         self.add_obstacle(2010, 200, 10, 100)
#         self.add_obstacle(582.5, 85, 24, 15)
#         self.add_obstacle(1157.5, 85, 89, 15)
#         self.add_obstacle(1695, 85, 303, 15)
#         self.add_obstacle(1605, 165, 30, 65)
#         self.add_obstacle(1647.5, 132, 14, 35)
#         self.add_enemy(3, Spark)
#         self.add_enemy(1, Laser)
#         self.add_enemy(1, Hothead)
#         game_world.add_objects(self.enemys, 1)
#         print('ENTER STAGE2')

#     @staticmethod
#     def exit(self, event):
#         print('EXIT STAGE2')

#     @staticmethod
#     def do(self):
#         server.player.x = clamp(0, server.player.x, 2000)
#         server.player.screen_x = clamp(20, server.player.screen_x, 780)

#         if server.player.x >= 400 and server.player.x < 1600 and server.player.can_move:
#             self.x = 400 - server.player.x

#             if server.player.dir != 0 and server.player.can_move:
#                 if server.player.isDash == False:
#                     for ob in self.obstacles:
#                         ob.x -= server.player.dir * \
#                             RUN_SPEED_PPS * game_framework.frame_time
#                 else:
#                     for ob in self.obstacles:
#                         ob.x -= server.player.dir * 2 * \
#                             RUN_SPEED_PPS * game_framework.frame_time

#         self.x = clamp(-1600, self.x, 0)

#     @staticmethod
#     def draw(self):
#         self.background_image.clip_draw_to_origin(
#             0, 0, 1100, 450, self.x / 5, 0)
#         self.land_image.clip_draw_to_origin(0, 0, 2000, 300, self.x, -2)

# class STAGE_3:
#     @staticmethod
#     def enter(self, event):
#         self.prev_portal = [600, 90, 650, 140]
#         self.next_portal = [0, 0, 0, 0]
#         print('ENTER STAGE3')

#     @staticmethod
#     def exit(self, event):
#         print('EXIT STAGE3')

#     @staticmethod
#     def do(self):
#         pass

#     @staticmethod
#     def draw(self):
#         pass


next_state = {
    # STAGE_1:   {NEXT: STAGE_2},
    # STAGE_2:   {PREV: STAGE_1, NEXT: STAGE_3},
    # STAGE_3:   {PREV: STAGE_2},
}


class Stage:
    def __init__(self):
        self.event_que = []
        self.obstacles = []
        self.cur_state = STAGE_1
        self.cur_state.enter(self, None)
        self.x, self.y = 0, 0
        self.type = 0

        
    def update(self):
        self.cur_state.do(self)
        max = 0
        for ob in self.obstacles:
            if server.player.screen_x > ob.x - ob.w - server.player.w + 10 and \
               server.player.screen_x < ob.x + ob.w + server.player.w - 10:
                if ob.y + ob.h > max:
                    max = ob.y + ob.h + server.player.h
                server.player.cur_floor = max

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(
                    f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        for ob in self.obstacles:
            draw_rectangle(*ob.get_bb())
    
    def add_obstacle(self, x, y, w, h):
        self.obstacles.append(Obstacle(x, y, w, h))

    def add_enemy(self, num, TYPE):
        for n in range(num):
            server.enemy.append(TYPE())

    def add_event(self, event):
        self.event_que.insert(0, event)