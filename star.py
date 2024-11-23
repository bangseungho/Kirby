from pico2d import *
from enemy import Enemy
import game_framework


class Star:
    image = None
    effect = None
    clush = None
    rotate = 0
    frame = 0

    def __init__(self, x=2000, y=3000, velocity=1):
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
        self.type = 5

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
        self.x += self.velocity
        self.ex, self.ey = self.x + 15 * -1 * self.velocity, self.y
        self.frame = (self.frame + 5 * game_framework.frame_time) % 3

        if self.isCrush:
            self.cframe = (self.cframe + 15 * game_framework.frame_time)

        if self.velocity > 0:
            self.face_dir = 1
        elif self.velocity < 0:
            self.face_dir = -1

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
