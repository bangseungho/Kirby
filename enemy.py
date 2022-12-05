from pico2d import *
from enum import Enum
import game_framework
import player_speed
import random
import math
import game_world

import server

TIMER, TURN, PATROL, DAMAGED, SUCKED, JATTACK, SATTACK = range(7)
event_name = ['TIMER', 'TURN', 'PATROL', 'DAMAGED', 'SUCKED', 'JATTACK', 'SATTACK']

class DEATH:
    @staticmethod
    def enter(self, event):
        self.frame = 0
        if self.type == 2:
            self.set_speed(3, 2)
            self.set_image(24, 18, 166)
        if self.type == 3:
            self.set_speed(3, 1)
            self.set_image(19, 19, 80)
        if self.type == 4:
            self.set_speed(3, 1)
            self.set_image(23, 21, 84)

    @staticmethod
    def exit(self, event):
        self.isDeath = True
        pass

    @staticmethod
    def do(self):
        self.face_dir = self.dir_damge

        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        self.x += self.dir_damge / 10

        self.death_timer -= 1

        if self.death_timer == 0:
            game_world.remove_object(self)

    def draw(self):
        if self.death_timer > 500:
            self.scomposite_draw()
        elif self.death_timer % 2 == 0:
            self.scomposite_draw()



class PULL:
    def enter(self, event):
        self.frame = 0
        if self.type == 2:
            self.set_speed(1.3, 1)
            self.set_image(24, 18, 166)
        if self.type == 3:
            self.set_speed(1.5, 1)
            self.set_image(19, 19, 80)
        if self.type == 4:
            self.set_speed(1.5, 1)
            self.set_image(23, 21, 84)
            
    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.face_dir = -server.player.face_dir

        if self.x < server.player.screen_x:
            self.x += self.RUN_SPEED_PPS * game_framework.frame_time * 1.3
        else:
            self.x -= self.RUN_SPEED_PPS * game_framework.frame_time * 1.3
        if self.y < server.player.y:
            self.y += self.RUN_SPEED_PPS * game_framework.frame_time * 1.3
        else:
            self.y -= self.RUN_SPEED_PPS * game_framework.frame_time * 1.3

    def draw(self):
        self.scomposite_draw()


class Enemy:
    def __init__(self, x, y, w, h, image_posY, cur_state, TYPE):
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
        self.type = TYPE
        self.isDeath = False
        self.death_cnt = 0

    def with_player(self):
       if server.player.dir != 0 and \
           server.player.x > 400 and server.player.x < 1600:
            if server.player.isDash == False:
                self.x -= server.player.dir * \
                    player_speed.RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= server.player.dir * 2 * \
                    player_speed.RUN_SPEED_PPS * game_framework.frame_time

    def update(self):
        self.cur_state.do(self)

        self.dis_to_player = abs(self.x - server.player.screen_x)
        self.height_to_player = abs(self.y - server.player.y)

        if self.type != 10:
            self.with_player()

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
    
    def scomposite_draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(
                self.frame) * self.w, self.image_posY, self.w, self.h, 0, ' ', self.x, self.y, self.w * 2, self.h * 2)
        else:
            self.image.clip_composite_draw(int(
                self.frame) * self.w, self.image_posY, self.w, self.h, 0, 'h', self.x, self.y, self.w * 2, self.h * 2)
        if self.type == 10 and self.life > 0:
            self.hp.clip_composite_draw(int(10 - self.life) * 142 , 0, 142 , 17, 0, ' ', 400, 50, 400, 34)
            self.icon.draw(750, 50, 100, 100)



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
