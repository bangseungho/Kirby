from pico2d import *
import game_world
import game_framework
from player_speed import *
from spark import Spark
from laser import Laser
from hothead import Hothead
from dedede import Dedede
from enemy import Enemy
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
        self.stype = 1
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
        for a in server.enemy:
            a.x = -999999
            a.y = -999999
        for a in server.stage.obstacles:
            a.x = -999999
            a.y = -999999

        game_world.clear()
        server.enemy.clear()
        self.obstacles.clear()

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

        self.sx, self.sy = self.canvas_width//2 - self.window_left / \
            10, self.canvas_height//2 - self.window_bottom

        self.background_image.draw(self.sx, self.sy, 1125, 500)

        self.land_image.clip_draw_to_origin(
            self.window_left, self.window_bottom, self.canvas_width, self.canvas_height, 0, 0,
            self.canvas_width, self.canvas_height / 1.5
        )


class STAGE_2:
    @staticmethod
    def enter(self, event):
        self.stype = 2
        self.frame = 0
        game_world.add_object(server.stage, 0)
        game_world.add_object(server.player, 1)

        server.stage.window_left = 0
        server.player.y = 400
        server.player.x = 400
        server.player.screen_x = 400
        server.player.sx = 400

        self.background_image = load_image('resource/stage1_background.png')
        self.land_image = load_image('resource/stage2_land.png')
        self.add_obstacle(400, 60, 400, 40)

        self.add_enemy(1, Dedede)
        game_world.add_objects(server.enemy, 1)

        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = 800
        self.h = self.land_image.h
        self.y = self.canvas_height // 2

        

        game_world.add_collision_pairs(
            server.player, self.obstacles, 'player:ob')
        # self.add_enemy(1, Spark)

        print('ENTER STAGE1')

    @staticmethod
    def exit(self, event):
        print('EXIT STAGE1')

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * 2.5 *
                ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    @staticmethod
    def draw(self):
        self.land_image.clip_composite_draw(int(
            self.frame) * 255, 0, 255, 190, 0, ' ', 400, self.y, 810, 455)


next_state = {
    STAGE_1:   {NEXT: STAGE_2},
    STAGE_2:   {PREV: STAGE_1},
}


class Stage:
    def __init__(self):
        self.event_que = []
        self.obstacles = []
        self.cur_state = STAGE_1
        self.cur_state.enter(self, None)
        self.x, self.y = 0, 0
        self.type = 0
        self.stype = 1

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

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHTBRACKET:
                self.add_event(NEXT)
            if event.key == SDLK_LEFTBRACKET:
                self.add_event(PREV)
