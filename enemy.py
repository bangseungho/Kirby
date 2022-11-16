from pico2d import *
from enum import Enum
import play_state
import game_framework
import player_speed
import random

TIMER, TURN, PATROL, DAMAGED = range(4)
event_name = ['TIMER', 'TURN', 'PATROL', 'DAMAGED']

class EnemyType(Enum):
    Spark = 0
    Laser = 1
    Hothead = 2


class Enemy:
    def __init__(self, x, y, w, h, image_posY, cur_state):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.image_posY = image_posY
        self.dir = random.randint(-1, 1)
        self.face_dir = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = cur_state
        self.cur_state.enter(self, None)
        self.next_state = {}
        self.timer = random.randint(1000, 1500)
        self.cooltime = 0
        self.dis_to_player = 1000
        self.height_to_player = 1000
        self.PIXEL_PER_METER = (10.0 / 0.3)
        self.RUN_SPEED_KMPH = 12.0
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)
        self.TIME_PER_ACTION = 1.3
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 4
        self.dir_damge = 0
        self.isSuck = False
        self.death_timer = 1000

    def update(self):
        self.cur_state.do(self)

        self.dis_to_player = abs(self.x - play_state.player.screen_x)
        self.height_to_player = abs(self.y - play_state.player.y)

        if play_state.player.dir != 0 and \
           play_state.player.x > 400 and play_state.player.x < 1600:
            if play_state.player.isDash == False:
                self.x -= play_state.player.dir * \
                    player_speed.RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= play_state.player.dir * 2 * \
                    player_speed.RUN_SPEED_PPS * game_framework.frame_time



        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = self.next_state[self.cur_state][event]
            except KeyError:
                print(
                    f'ERROR: State {self.cur_state.__name__}    Event {self.event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        debug_print('pppp')
        debug_print(f'Face Dir: {self.face_dir}, Dir: {self.dir}')
        draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def set_speed(self, time_per_action, frames_per_action):
        self.TIME_PER_ACTION = time_per_action
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = frames_per_action

    def set_image(self, width, height, image_posY):
        self.w = width
        self.h = height
        self.image_posY = image_posY

    def get_bb(self):
        return self.x - self.w, self.y - self.h, \
            self.x + self.w, self.y + self.h

    def handle_collision(self, other, group):
        pass