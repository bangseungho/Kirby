from pico2d import *
import game_world
import game_framework


class Breath:
    image = None
    frame = 0

    def __init__(self, x=400, y=300, velocity=1, face=0):
        if Breath.image == None:
            Breath.image = load_image('resource/breath.png')
        self.x, self.y, self.velocity = x + 1 * velocity * 20, y, velocity
        self.face_dir = face

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 33, 0,
                                           33, 19, 0, ' ', self.x, self.y, 33, 19)
        else:
            self.image.clip_composite_draw(int(self.frame) * 33, 0,
                                           33, 19, 0, 'h', self.x, self.y, 33, 19)

    def update(self):
        self.x += self.velocity / 3
        self.frame = (self.frame + 20 * game_framework.frame_time)

        if self.frame == 9:
            game_world.remove_object(self)
