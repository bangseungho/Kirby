from pico2d import *
from enemy import *
from enum import Enum
import kirby
import random
import game_framework
import game_world

VELOCITY = 5
MASS = 10

class Dstar:
    image = None
    rotate = 0
    frame = 0

    def __init__(self, x= 400, y=300 , velocity=1):
        if Dstar.image == None:
            Dstar.image = load_image('resource/dedede_star.png')
        self.x, self.y, self.velocity = x + 1 * velocity * 20, y, velocity
        self.x -= VELOCITY * 20
        self.isFire = False
        self.isCrush = False
        self.face_dir = 1
        self.w = 32
        self.h = 32
        self.type = 11

    def draw(self):
        self.image.clip_composite_draw(int(
                        self.frame) * self.w, 0, 32, 32, self.rotate, ' ', self.x, self.y, 50, 50)
        
    def update(self):
        self.frame = (self.frame + 7 * game_framework.frame_time)

        if int(self.frame) == 7:
            self.frame = 3

        self.rotate += 0.02

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, other, group):
        if group == 'star:enemy':
            self.cx, self.cy = other.x, other.y

# class RUN:
#     @staticmethod
#     def enter(self, event):
#         self.y = 155
#         if self.dir == 0:
#             self.dir = 1
#         self.timer = -1
#         self.set_speed(1.3, 4)
#         self.set_image(70, 70, 110)
#         pass

#     @staticmethod
#     def exit(self, event):
#         pass

#     @staticmethod
#     def do(self):
#         self.frame = (self.frame + self.FRAMES_PER_ACTION *
#                       self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION
#         if self.dis_to_player <= 150 and self.y > server.player.y:
#             self.add_event(CATTACK)

#     def draw(self):
#         self.scomposite_draw()
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
            self.make_star()
            if server.player.y < 150:
                server.player.damaged(5)
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
        self.life = 20
        self.timer = random.randint(1000, 1500)
        self.next_state = {
            RUN:  {PATROL: ATTACK, DAMAGED: DEATH, SUCKED: RUN, CATTACK: ATTACK},
            ATTACK: { TURN: RUN, DAMAGED: DEATH, SUCKED: ATTACK, PATROL: RUN},
            DEATH : { TURN: DEATH, PATROL: DEATH, DAMAGED: DEATH, SUCKED: DEATH },
            PULL : { TURN: RUN, PATROL: RUN, DAMAGED: DEATH, SUCKED: PULL }
        }

    def handle_collision(self, other, group):
        if group == 'star:enemy':
            self.life -= 1
        if group == 'player:enemy':
            if other.cur_state == kirby.ABILITY and not self.isDeath:
                self.add_event(DAMAGED)
                if self.x < other.screen_x:
                    self.dir_damge = -1
                else:
                    self.dir_damge = 1
    
    def make_star(self):
        dstar = Dstar(self.x, 155, self.face_dir*2)
        game_world.add_object(dstar, 1)
        game_world.add_collision_pairs(dstar, None, 'star:enemy')
        game_world.add_collision_pairs(dstar, None, 'star:ob')