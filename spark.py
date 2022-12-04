from pico2d import *
from enemy import *
from enum import Enum
import kirby
import random
import game_framework
import game_world


class RUN:
    @staticmethod
    def enter(self, event):
        if self.dir == 0:
            self.dir = 1
        self.timer = -1
        self.set_speed(1.3, 4)
        self.set_image(24, 19, 0)
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.face_dir = self.dir
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        self.y -= self.RUN_SPEED_PPS * game_framework.frame_time * 1.5
        if self.y < 90:
            self.y = 90

        if self.dis_to_player <= 100 and self.y > server.player.y:
            if self.x < server.player.screen_x:
                self.dir = 1
            else:
                self.dir = -1
        
        if self.dis_to_player <= 60 and self.cooltime == 0:
            self.add_event(PATROL)

        self.x += self.dir * self.RUN_SPEED_PPS * game_framework.frame_time
        self.timer -= 1
        
        if self.cooltime > 0:
            self.cooltime -= 1
        
        if self.timer == 0:
            self.add_event(TIMER)
        

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
        self.frame = 0
        self.set_speed(1.3, 15)
        self.set_image(64, 64, 38)
        pass

    @staticmethod
    def exit(self, event):
        self.cooltime = 1000
        pass

    @staticmethod
    def do(self):
        self.face_dir = self.dir
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time)
        
        if int(self.frame) == 15:
            self.add_event(TURN)

    def draw(self):
        self.scomposite_draw()


class Spark(Enemy):
    image = None

    def __init__(self):
        super(Spark, self).__init__(random.randint(800, 1000), 90, 24, 19, 0, RUN, 2)
        if Spark.image == None:
            Spark.image = load_image("resource/spark.png")
        self.temp_dir = 1
        self.timer = random.randint(1000, 1500)
        self.next_state = {
            RUN:  { TIMER: JUMP, PATROL: ATTACK, DAMAGED: DEATH, SUCKED: PULL },
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