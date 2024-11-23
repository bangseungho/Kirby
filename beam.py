from pico2d import *
import game_framework

class KBeam:
    image = None

    def __init__(self, x=800, y=1000, velocity=0, face_dir = 1):
        if KBeam.image == None:
            KBeam.image = load_image('resource/kirby_beam.png')
        self.x, self.y, self.velocity, self.face_dir = x, y, velocity, face_dir
        self.frame = 0
        self.type = 9
        self.FRAMES_PER_ACTION = 4
        self.ACTION_PER_TIME = 2
        
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(
                self.frame) * 56, 0, 56, 5, 0, ' ', self.x, self.y, 56 * 2, 5 * 2)
        else:
            self.image.clip_composite_draw(int(
                self.frame) * 56, 0, 56, 5, 0, 'h', self.x, self.y, 56 * 2, 5 * 2)

    def update(self):
        self.frame = (self.frame + self.FRAMES_PER_ACTION *
                      self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION


        self.x += self.velocity * 2

    def get_bb(self):
        return self.x - 56, self.y - 4, self.x + 56, self.y + 4

    def handle_collision(self, other, group):
        if group == 'kbeam:enemy':
            self.x = 800
            self.y = 1000
            self.velocity = 0
        pass
            