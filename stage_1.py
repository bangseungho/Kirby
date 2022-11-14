from pico2d import *
import game_world
import game_framework
import play_state

NEXT, PREV, UD = range(3)

event_name = ['NEXT', 'PREV', 'UD']

cnt = 0

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Obstacle:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top
    
    def handle_collision(self, other, group):
        if group == 'star:ob':
            pass
        pass


class STAGE_1:
    obstacle = []

    @staticmethod
    def enter(self, event):
        self.background_image = load_image('stage1_background.png')
        self.land_image = load_image('stage1_land.png')
        self.next_portal = [600, 90, 650, 140]
        self.prev_portal = [0, 0, 0, 0]
        STAGE_1.obstacle.append(Obstacle(582.5, 79, 27.5, 110))
        STAGE_1.obstacle.append(Obstacle(1065, 79, 1250, 110))
        STAGE_1.obstacle.append(Obstacle(1390, 79, 2000, 110))
        STAGE_1.obstacle.append(Obstacle(1580, 110, 1630, 240))
        STAGE_1.obstacle.append(Obstacle(1630, 110, 1665, 180))
        print('ENTER STAGE1')

    @staticmethod
    def exit(self, event):
        print('EXIT STAGE1')

    @staticmethod
    def do(self):
        play_state.player.x = clamp(0, play_state.player.x, 2000)
        play_state.player.screen_x = clamp(20, play_state.player.screen_x, 780)

        if play_state.player.x >= 400 and play_state.player.x < 1600:
            self.x = 400 - play_state.player.x

            if play_state.player.dir != 0:
                if play_state.player.isDash == False:
                    for ob in STAGE_1.obstacle:
                        ob.left -= play_state.player.dir * \
                            RUN_SPEED_PPS * game_framework.frame_time
                        ob.right -= play_state.player.dir * \
                            RUN_SPEED_PPS * game_framework.frame_time
                else:
                    for ob in STAGE_1.obstacle:
                        ob.left -= play_state.player.dir * 2 * \
                            RUN_SPEED_PPS * game_framework.frame_time
                        ob.right -= play_state.player.dir * 2 * \
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
        self.background_image = load_image('stage1_background.png')
        self.land_image = load_image('stage2_land.png')
        self.next_portal = [600, 90, 650, 140]
        self.prev_portal = [200, 90, 250, 140]
        print('ENTER STAGE2')

    @staticmethod
    def exit(self, event):
        print('EXIT STAGE2')

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        self.background_image.draw(500, 450 // 2, 1100, 450)
        self.land_image.draw(1000, 253, 2000, 524)

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
        self.cur_state = STAGE_1
        self.cur_state.enter(self, None)
        self.x, self.y = 0, 0
        self.next_portal = [0, 0, 0, 0]
        self.prev_portal = [0, 0, 0, 0]
        self.background_image = load_image('stage1_background.png')
        self.land_image = load_image('stage1_land.png')

    def update(self):
        self.cur_state.do(self)

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
        # draw_rectangle(self.cur_state.obstacles[0])
        for ob in self.cur_state.obstacle:
            draw_rectangle(ob.left, ob.bottom, ob.right, ob.top)
        

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
            self.add_event(NEXT)
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFTBRACKET:
            self.add_event(PREV)
