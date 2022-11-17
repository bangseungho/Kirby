from pico2d import *
from enemy import *
from enum import Enum
import random
import game_framework
import game_world
import time

class Fire:
    def __init__(self, x, y, face_dir):
        self.image = load_image("resource/hothead_fire.png")
        self.x = x
        self.y = y
        self.w = 60
        self.h = 25
        self.face_dir = face_dir
        self.frame = 0  
        self.FRAMES_PER_ACTION = 9
        self.ACTION_PER_TIME = 1.5
        self.timer = 1400
        self.re_frame = [8, 9, 2, 3, 7, 5, 0, 6, 4, 1]
        self.type = 7

    def draw(self):
        if self.face_dir == 1:
            for i in range(9):
                self.image.clip_composite_draw(int(
                    self.re_frame[i]) * self.w, 0, self.w, self.h, 0, ' ', self.x + self.face_dir * 63, self.y, self.w * 1.5, self.h * 1.5)
        if self.face_dir == -1:
            for i in range(9):
                self.image.clip_composite_draw(int(
                    self.re_frame[i]) * self.w, 0, self.w, self.h, 0, 'h', self.x + self.face_dir * 63, self.y, self.w * 1.5, self.h * 1.5)


    def get_bb(self):
        if self.face_dir == -1:
            return self.x + self.face_dir * 60 * 2, self.y - 25, self.x - 30, self.y + 25
        else:
            return self.x, self.y - 25, self.x + self.face_dir * 60 * 2, self.y + 25

    def update(self):
        self.timer -= 1

        for i in range(9):
            self.re_frame[i] = (self.re_frame[i] + self.FRAMES_PER_ACTION *
                        self.ACTION_PER_TIME * game_framework.frame_time) % 9
        
        Enemy.with_player(self)

    def handle_collision(self, other, group):
        other.damaged(3)

class RUN:
    @staticmethod
    def enter(self, event):
        self.timer = 1000
        self.set_speed(0.8, 5)
        self.set_image(22, 21, 0)
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.face_dir = self.dir
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION
        self.x += self.dir * self.RUN_SPEED_PPS * game_framework.frame_time
        self.timer -= 1

        if self.y > self.py:
            self.y = self.py
            self.y -= 1
        if self.y < self.py:
            self.y = self.py

        if self.timer == 0:
            self.add_event(TIMER)

    def draw(self):
        self.scomposite_draw()

class ATTACK:
    @staticmethod
    def enter(self, event):
        self.timer = 2000
        self.frame = 0
        self.set_speed(0.3, 5)
        self.set_image(24, 21, 42)
        pass

    @staticmethod
    def exit(self, event):
        for game_object in game_world.all_objects():
            if game_object.type == 7:
                game_world.remove_object(game_object)

    @staticmethod
    def do(self):
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time)
        
        if self.timer > 1500:
            if self.frame >= 3:
                self.frame = 0
        if self.timer == 1430:
            self.fire_hotfire()

        if int(self.frame) == 5:
            self.frame = 3

        if self.y > self.py:
            self.y = self.py
            self.y -= 1
        if self.y < self.py:
            self.y = self.py


        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)



    def draw(self):
        self.scomposite_draw()

class Hothead(Enemy):
    image = None

    def __init__(self):
        super(Hothead, self).__init__(1900, 125, 22, 21, 0, RUN, 4)
        if Hothead.image == None:
            Hothead.image = load_image("resource/hothead.png")
        self.beam_start_time = 0
        self.beam_end_time = 0
        self.next_state = {
            RUN:  { TIMER: ATTACK, DAMAGED: DEATH, SUCKED: PULL },
            ATTACK: { TURN: RUN, DAMAGED: DEATH, SUCKED: PULL, TIMER: RUN },
            DEATH : { TURN: DEATH, DAMAGED: DEATH, SUCKED: DEATH },
            PULL : { TURN: RUN, DAMAGED: DEATH, SUCKED: PULL }
        }
        self.set_speed(0.8, 5)
        self.set_image(22, 21, 0)
        self.timer = 1000
        self.dir = 1
        self.py = self.y

    def scomposite_draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(
                self.frame) * self.w, self.image_posY, self.w, self.h, 0, ' ', self.x, self.y, self.w * 2, self.h * 2)
        if self.face_dir == -1:
            self.image.clip_composite_draw(int(
                self.frame) * self.w, self.image_posY, self.w, self.h, 0, 'h', self.x, self.y, self.w * 2, self.h * 2)

    def fire_hotfire(self):
        fires = Fire(self.x, self.y, self.face_dir)
        game_world.add_object(fires, 0)
        game_world.add_collision_pairs(fires, play_state.stage.player, 'player:fire')

    def handle_collision(self, other, group):
        if group == 'star:enemy':
            self.add_event(DAMAGED)
            self.dir_damge = other.face_dir
        if group == 'enemy:ob':
            self.dir *= -1