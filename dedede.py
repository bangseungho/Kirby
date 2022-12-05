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
        self.x, self.y, self.velocity = x + 1 * velocity * 60, y - 20, velocity
        self.isFire = False
        self.isCrush = False
        self.face_dir = 1
        self.w = 32
        self.h = 32
        self.type = 11
        self.life = 3

    def draw(self):
        self.image.clip_composite_draw(int(
                        self.frame) * self.w, 0, 32, 32, self.rotate, ' ', self.x, self.y, 60, 60)
        
    def update(self):
        self.frame = (self.frame + 7 * game_framework.frame_time)
        self.life -= game_framework.frame_time

        if self.life < 0:
            game_world.remove_object(self)

        if int(self.frame) == 7:
            self.frame = 3

        self.rotate += 0.02

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, other, group):
        pass

class HURT:
    @staticmethod
    def enter(self, event):
        self.set_speed(1.3, 1)
        self.set_image(62, 62, 180)
        print(self.life)
        self.frame = 0
        self.timer = 200

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.x += self.dir_damge / 10
        self.timer -= 1
        if self.life <= 0:
            self.death_timer -= 1

            if self.death_timer == 0:
                game_world.remove_object(self)
        elif self.timer <= 0:
            self.add_event(TURN)

    def draw(self):
        if self.death_timer > 500:
            self.scomposite_draw()
        elif self.death_timer % 2 == 0:
            self.scomposite_draw()

class RUN:
    @staticmethod
    def enter(self, event):
        self.y = 155
        if self.dir == 0:
            self.dir = 1
        self.frame = 0
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
       
        
        if self.dis_to_player <= 300 and self.height_to_player <= 100:
            self.set_speed(1.3, 4)
            self.set_image(80, 80, 242)
            if self.x < server.player.screen_x:
                self.dir = 1
            else:
                self.dir = -1
            self.x += self.dir * self.RUN_SPEED_PPS * game_framework.frame_time
        else:
            self.set_speed(1.3, 4)
            self.set_image(70, 70, 110)
        
        if self.dis_to_player <= 150 and self.height_to_player <= 100:
            randValue = random.randint(1, 2)
            if randValue == 1:
                self.add_event(JATTACK)
            elif randValue == 2:
                self.add_event(SATTACK)


        self.face_dir = self.dir

    def draw(self):
        self.scomposite_draw()


class STRONGATTACK:
    @staticmethod
    def enter(self, event):
        self.timer = 1300
        self.y = 165
        self.frame = 0
        self.set_speed(1.3, 8)
        self.set_image(150, 150, 322)
        pass

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                self.ACTION_PER_TIME * game_framework.frame_time)

        if self.x < server.player.screen_x:
            self.dir = 1
        else:
            self.dir = -1
        self.x += self.dir * self.RUN_SPEED_PPS * game_framework.frame_time * 2

        if int(self.frame) == 8:
            self.add_event(TURN)

        self.face_dir = self.dir

    def draw(self):
        self.scomposite_draw()


class JUMPATTACK:
    @staticmethod
    def enter(self, event):
        self.timer = 1300
        self.v = VELOCITY
        self.m = MASS
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
            if self.v <= 0 and self.y >= 185:
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
            self.hp = load_image("resource/dedede_hp.png")
            self.icon = load_image("resource/dedede_icon.png")
        self.temp_dir = 1
        self.v, self.m = VELOCITY, MASS
        self.JUMP_HEIGHT = 0.0022
        self.life = 10
        self.timer = random.randint(1000, 1500)
        self.next_state = {
            RUN:  {PATROL: JUMPATTACK, DAMAGED: HURT, JATTACK: JUMPATTACK, SATTACK: STRONGATTACK},
            JUMPATTACK: { TURN: RUN, DAMAGED: HURT, },
            STRONGATTACK: { TURN: RUN, DAMAGED: HURT, },
            PULL : { TURN: RUN, PATROL: RUN, DAMAGED: DEATH,  },
            HURT : { TURN: RUN, PATROL: RUN, DAMAGED: HURT, JATTACK: JUMPATTACK, SATTACK: STRONGATTACK}
        }

    def handle_collision(self, other, group):
        if group == 'star:enemy':
            self.add_event(DAMAGED)
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