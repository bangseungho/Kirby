from pico2d import *
from enemy import Enemy
import game_world
import game_framework
import kirby
import play_state
import player_speed


class Star:
    image = None
    effect = None
    clush = None
    rotate = 0
    frame = 0

    def __init__(self, x=400, y=300, velocity=1):
        if Star.image == None:
            Star.image = load_image('resource/star.png')
        if Star.effect == None:
            Star.effect = load_image('resource/spit.png')
        if Star.clush == None:
            Star.clush = load_image('resource/spit2.png')
        self.x, self.y, self.velocity = x + 1 * velocity * 20, y, velocity
        self.ex, self.ey = x, y
        self.cx, self.cy = 0, 0
        self.isFire = False
        self.isCrush = False
        self.face_dir = 1
        self.cframe = 0

    def draw(self):
        if self.isFire:
            self.image.clip_composite_draw(37, 37,
                                        37, 37, self.rotate, ' ', self.x, self.y, 37, 37)
            self.effect.clip_composite_draw(int(self.frame) * 16 , 16,
                                        16, 16, 0, ' ', self.ex, self.ey, 32, 32)
        if self.isCrush:
            self.clush.clip_composite_draw(int(self.cframe) * 42 , 0,
                                        42, 42, 0, ' ', self.cx, self.cy, 50, 50)
        
    def update(self):
        self.x += self.velocity / 1.5
        self.ex, self.ey = self.x + 15 * -1 * self.velocity, self.y
        self.frame = (self.frame + 5 * game_framework.frame_time) % 3

        if self.isCrush:
            self.cframe = (self.cframe + 15 * game_framework.frame_time)

        if self.velocity > 0:
            self.face_dir = 1
        elif self.velocity < 0:
            self.face_dir = -1

        Enemy.with_player(self)

        if play_state.player.dir != 0 and \
           play_state.player.x > 400 and play_state.player.x < 1600:
            if play_state.player.isDash == False:
                self.cx -= play_state.player.dir * \
                                player_speed.RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.cx -= play_state.player.dir * 2 *\
                                player_speed.RUN_SPEED_PPS * game_framework.frame_time

        if self.x < 400:
            self.rotate += 0.02
        else:
            self.rotate -= 0.02

    def get_bb(self):
        return self.x - 19, self.y - 19, self.x + 19, self.y + 19

    def handle_collision(self, other, group):
        if group == 'star:ob':
            self.cx, self.cy = self.x, self.y
        if group == 'star:enemy':
            self.cx, self.cy = other.x, other.y

        self.x, self.y, self.velocity = -100, -1000, 0
        self.isFire = False
        self.isCrush = True
        self.cframe = 0
