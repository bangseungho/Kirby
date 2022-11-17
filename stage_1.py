from pico2d import *
import game_world
import game_framework
import play_state
from player_speed import *
from spark import Spark
from laser import Laser
from hothead import Hothead
from kirby import Kirby

NEXT, PREV, UD = range(3)

event_name = ['NEXT', 'PREV', 'UD']

cnt = 0

class Obstacle:
    def __init__(self, x, y, w, h):
        self.px, self.py = x, y
        self.x, self.y = x, y
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
        self.next_portal = [600, 90, 650, 140]
        self.prev_portal = [0, 0, 0, 0]
        self.add_obstacle(800, 38, 800, 30)
        self.add_obstacle(2010, 200, 10, 100)
        self.add_obstacle(582.5, 85, 24, 15)
        self.add_obstacle(1157.5, 85, 89, 15)
        self.add_obstacle(1695, 85, 303, 15)
        self.add_obstacle(1605, 165, 30, 65)
        self.add_obstacle(1647.5, 132, 14, 35)
        self.add_enemy(3, Spark)
        self.add_enemy(1, Laser)
        self.add_enemy(1, Hothead)
        game_world.add_objects(self.enemys, 1)
        print('ENTER STAGE1')

    @staticmethod
    def exit(self, event):
        print('EXIT STAGE1')

    @staticmethod
    def do(self):
        self.player.x = clamp(0, self.player.x, 2000)
        self.player.screen_x = clamp(20, self.player.screen_x, 780)

        if self.player.x >= 400 and self.player.x < 1600 and self.player.can_move:
            self.x = 400 - self.player.x

            if self.player.dir != 0 and self.player.can_move:
                if self.player.isDash == False:
                    for ob in self.obstacles:
                        ob.x -= self.player.dir * \
                            RUN_SPEED_PPS * game_framework.frame_time
                else:
                    for ob in self.obstacles:
                        ob.x -= self.player.dir * 2 * \
                            RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(-1600, self.x, 0)

    @staticmethod
    def draw(self):
        self.background_image.clip_draw_to_origin(
            0, 0, 1100, 450, self.x / 5, 0)
        self.land_image.clip_draw_to_origin(0, 0, 2000, 300, self.x, -2)

class STAGE_2:
    @staticmethod
    def enter(self, event):
        self.background_image = load_image('resource/stage1_background.png')
        self.land_image = load_image('resource/stage1_land.png')
        self.next_portal = [600, 90, 650, 140]
        self.prev_portal = [0, 0, 0, 0]
        self.add_obstacle(800, 38, 800, 30)
        self.add_obstacle(2010, 200, 10, 100)
        self.add_obstacle(582.5, 85, 24, 15)
        self.add_obstacle(1157.5, 85, 89, 15)
        self.add_obstacle(1695, 85, 303, 15)
        self.add_obstacle(1605, 165, 30, 65)
        self.add_obstacle(1647.5, 132, 14, 35)
        self.add_enemy(3, Spark)
        self.add_enemy(1, Laser)
        self.add_enemy(1, Hothead)
        game_world.add_objects(self.enemys, 1)
        print('ENTER STAGE1')

    @staticmethod
    def exit(self, event):
        print('EXIT STAGE1')

    @staticmethod
    def do(self):
        play_state.player.x = clamp(0, play_state.player.x, 2000)
        play_state.player.screen_x = clamp(20, play_state.player.screen_x, 780)

        if play_state.player.x >= 400 and play_state.player.x < 1600 and play_state.player.can_move:
            self.x = 400 - play_state.player.x

            if play_state.player.dir != 0 and play_state.player.can_move:
                if play_state.player.isDash == False:
                    for ob in self.obstacles:
                        ob.x -= play_state.player.dir * \
                            RUN_SPEED_PPS * game_framework.frame_time
                else:
                    for ob in self.obstacles:
                        ob.x -= play_state.player.dir * 2 * \
                            RUN_SPEED_PPS * game_framework.frame_time

        self.x = clamp(-1600, self.x, 0)

    @staticmethod
    def draw(self):
        self.background_image.clip_draw_to_origin(
            0, 0, 1100, 450, self.x / 5, 0)
        self.land_image.clip_draw_to_origin(0, 0, 2000, 300, self.x, -2)

class STAGE_3:
    @staticmethod
    def enter(self, event):
        self.prev_portal = [600, 90, 650, 140]
        self.next_portal = [0, 0, 0, 0]
        print('ENTER STAGE3')

    @staticmethod
    def exit(self, event):
        print('EXIT STAGE3')

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        pass


next_state = {
    STAGE_1:   {NEXT: STAGE_2},
    STAGE_2:   {PREV: STAGE_1, NEXT: STAGE_3},
    STAGE_3:   {PREV: STAGE_2},
}


class Stage:
    def __init__(self):
        self.event_que = []
        self.obstacles = []
        self.enemys = []
        self.cur_state = STAGE_1
        self.cur_state.enter(self, None)
        self.x, self.y = 0, 0
        self.next_portal = [0, 0, 0, 0]
        self.prev_portal = [0, 0, 0, 0]
        self.background_image = load_image('resource/stage1_background.png')
        self.land_image = load_image('resource/stage1_land.png')
        self.type = 0
        self.player = Kirby()
        game_world.add_object(self.player, 1)
        game_world.add_collision_pairs(self.player, self.enemys, 'player:enemy')
        game_world.add_collision_pairs(self.player, self.obstacles, 'player:ob')
        
    def update(self):
        self.cur_state.do(self)
        max = 0
        for ob in self.obstacles:
            if self.player.screen_x > ob.x - ob.w - self.player.w + 10 and \
               self.player.screen_x < ob.x + ob.w + self.player.w - 10:
                if ob.y + ob.h > max:
                    max = ob.y + ob.h + self.player.h
                self.player.cur_floor = max

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
        # for ob in self.obstacles:
        #     draw_rectangle(ob.x - ob.w, ob.y - ob.h, ob.x + ob.w, ob.y + ob.h)
    
    def add_obstacle(self, x, y, w, h):
        self.obstacles.append(Obstacle(x, y, w, h))

    def add_enemy(self, num, TYPE):
        for n in range(num):
            self.enemys.append(TYPE())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def in_portal(self, player_x, player_y):
        if player_x > self.next_portal[0] and player_x < self.next_portal[2] and \
           player_y > self.next_portal[1] and player_y < self.next_portal[3]:
            return 1
        if player_x > self.prev_portal[0] and player_x < self.prev_portal[2] and \
           player_y > self.prev_portal[1] and player_y < self.prev_portal[3]:
            return -1

    def move_stage(self, event, player_x, player_y):
        if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if self.in_portal(player_x, player_y) == 1:
                self.add_event(NEXT)
            elif self.in_portal(player_x, player_y) == -1:
                self.add_event(PREV)
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHTBRACKET:
            game_world.clear()

            self.add_event(NEXT)
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFTBRACKET:
            self.add_event(PREV)
