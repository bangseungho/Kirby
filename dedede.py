from pico2d import *
from enemy import *
from enum import Enum
import kirby
import random
import game_framework
import game_world

VELOCITY = 5
MASS = 10

class RUN:
    @staticmethod
    def enter(self, event):
        self.y = 155
        if self.dir == 0:
            self.dir = 1
        self.timer = -1
        self.set_speed(1.3, 4)
        self.set_image(70, 70, 110)
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION
        if self.dis_to_player <= 150 and self.y > server.player.y:
            self.add_event(CATTACK)

    def draw(self):
        self.scomposite_draw()

class JUMP:
    @staticmethod
    def enter(self, event):
        self.set_speed(1.5, 2)
        self.temp_dir = 1
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.face_dir = self.dir
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        self.x += self.dir * self.RUN_SPEED_PPS * game_framework.frame_time * 1.3

        if self.y > 160:
            self.temp_dir *= -1
        
        if self.y < 90:
            self.y = 90
            self.add_event(TURN)
            
        self.y += self.temp_dir * self.RUN_SPEED_PPS * game_framework.frame_time * 1.5


    def draw(self):
        self.scomposite_draw()


class ATTACK:
    @staticmethod
    def enter(self, event):
        self.timer = 1300
        self.v = VELOCITY
        self.y = 185
        self.frame = 0
        self.set_speed(1.3, 3)
        self.set_image(120, 110, 0)
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        if self.timer > 800:
            self.frame = 0
        else:
            if self.v <= 0 and self.y >= 210:
                self.frame = 2

                F = -((self.RUN_SPEED_PPS * game_framework.frame_time)
                    * self.m * (self.v ** 2)) / 20
                self.y += round(F)
                self.v -= 0.03
            
            if self.v > 0:
                self.frame = 1
                F = ((self.RUN_SPEED_PPS * self.JUMP_HEIGHT)
                        * self.m * (self.v ** 2)) / 20
                self.y += round(F)
                self.v -= 0.02

        if self.timer == 300:
            server.stage.y += 5
        if self.timer == 290:
            server.stage.y -= 5
        if self.timer == 280:
            server.stage.y += 5
        if self.timer == 270:
            server.stage.y -= 5
        if self.timer == 260:
            server.stage.y += 5
        if self.timer == 250:
            server.stage.y -= 5

        self.timer -= 1

        if self.timer < 0:
            self.add_event(TURN)

    def draw(self):
        self.scomposite_draw()


class Dedede(Enemy):
    image = None

    def __init__(self):
        super(Dedede, self).__init__(600, 155, 70, 70, 0, RUN, 10)
        if Dedede.image == None:
            Dedede.image = load_image("resource/dedede.png")
        self.temp_dir = 1
        self.v, self.m = VELOCITY, MASS
        self.JUMP_HEIGHT = 0.0022
        self.timer = random.randint(1000, 1500)
        self.next_state = {
            RUN:  { TIMER: JUMP, PATROL: ATTACK, DAMAGED: DEATH, SUCKED: PULL, CATTACK: ATTACK},
            JUMP: { TURN: RUN, PATROL: ATTACK, DAMAGED: DEATH, SUCKED: PULL },
            ATTACK: { TURN: RUN, DAMAGED: DEATH, SUCKED: PULL, PATROL: RUN},
            DEATH : { TURN: DEATH, PATROL: DEATH, DAMAGED: DEATH, SUCKED: DEATH },
            PULL : { TURN: RUN, PATROL: RUN, DAMAGED: DEATH, SUCKED: PULL }
        }

    def handle_collision(self, other, group):
        if group == 'enemy:ob':
            self.dir *= -1
            self.timer = random.randint(200, 400)
        if group == 'star:enemy':
            self.add_event(DAMAGED)
            self.dir_damge = other.face_dir
        if group == 'player:enemy':
            if other.cur_state == kirby.ABILITY and not self.isDeath:
                self.add_event(DAMAGED)
                if self.x < other.screen_x:
                    self.dir_damge = -1
                else:
                    self.dir_damge = 1
        if group == 'kbeam:enemy':
            self.add_event(DAMAGED)
            self.dir_damge = other.face_dir