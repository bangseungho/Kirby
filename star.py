from pico2d import *
import game_world
import game_framework
import kirby
import play_state

class Star:
    image = None
    effect = None
    rotate = 0
    frame = 0

    def __init__(self, x=400, y=300, velocity=1):
        if Star.image == None:
            Star.image = load_image('resource/star.png')
        if Star.effect == None:
            Star.effect = load_image('resource/spit.png')
        self.x, self.y, self.velocity = x + 1 * velocity * 20, y, velocity
        self.ex, self.ey = x, y

    def draw(self):
        self.image.clip_composite_draw(37, 37,
                                       37, 37, self.rotate, ' ', self.x, self.y, 37, 37)
        self.effect.clip_composite_draw(int(self.frame) * 16 , 16,
                                       16, 16, 0, ' ', self.ex, self.ey, 32, 32)
        
    def update(self):
        self.x += self.velocity / 1.5
        self.ex, self.ey = self.x + 15 * -1 * self.velocity, self.y
        self.frame = (self.frame + 5 * game_framework.frame_time) % 3
    
        if self.x < 400:
            self.rotate += 0.02
        else:
            self.rotate -= 0.02
        if self.x < 0 or self.x > 800:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 19, self.y - 19, self.x + 19, self.y + 19

    def handle_collision(self, other, group):
            game_world.remove_object(self)
            
