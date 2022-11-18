from pico2d import *
from enemy import *
from enum import Enum
import kirby
import random
import game_framework
import game_world
import time


class beam_laser:
    def __init__(self, x, y):
        self.image = load_image("resource/beam.png")
        self.x = x
        self.v = 100
        self.y = y
        self.type = 8

    def draw(self):
        self.image.draw(self.x - 50, self.y, 64, 8)

    def get_bb(self):
        return self.x - 32, self.y - 4, self.x + 32, self.y + 4

    def update(self):
        if self.x < 0:
            game_world.remove_object(self)
        self.x -= self.v * game_framework.frame_time * 10
        Enemy.with_player(self)

    def handle_collision(self, other, group):
        if group == 'beams:player':
            other.damaged(3)


class ATTACK:
    @staticmethod
    def enter(self, event):
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.beam_end_time = time.time()
        if self.dis_to_player <= 280 and play_state.player.screen_x < self.x:
            if self.beam_end_time - self.beam_start_time >= 1:
                self.frame = 0
                self.set_speed(1.0, 13)
                self.set_image(35, 21, 38)
                self.fire_beam_laser()
                self.beam_start_time = time.time()
        else:
            self.set_speed(1.3, 3)
            self.set_image(19, 19, 19)

        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        if self.y > 230 or self.y < 120:
            self.dir_y *= -1

        self.y += self.dir_y * 0.08

    def draw(self):
        self.scomposite_draw()


class Laser(Enemy):
    image = None

    def __init__(self):
        super(Laser, self).__init__(1550, 140, 24, 19, 0, ATTACK, 3)
        if Laser.image == None:
            Laser.image = load_image("resource/laser.png")
        self.beam_start_time = 0
        self.beam_end_time = 0
        self.next_state = {
            ATTACK: {SUCKED: PULL, DAMAGED: DEATH, },
            PULL:   {DAMAGED: DEATH, SUCKED: PULL, TURN: ATTACK},
            DEATH: {TURN: DEATH, DAMAGED: DEATH, SUCKED: DEATH}
        }
        self.set_speed(1.3, 3)
        self.set_image(19, 19, 19)
        self.face_dir = 1
        self.beams = []
        self.dir_y = 1

    def fire_beam_laser(self):
        self.beams.append(beam_laser(self.x, self.y))
        game_world.add_objects(self.beams, 1)
        game_world.add_collision_pairs(self.beams, play_state.player, 'beams:player')

    def handle_collision(self, other, group):
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
        pass