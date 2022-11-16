from pico2d import *
import game_world
import game_framework
import kirby
import play_state
import player_speed

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
        self.isFire = False
        self.face_dir = 1

    def draw(self):
        if self.isFire:
            self.image.clip_composite_draw(37, 37,
                                        37, 37, self.rotate, ' ', self.x, self.y, 37, 37)
            self.effect.clip_composite_draw(int(self.frame) * 16 , 16,
                                        16, 16, 0, ' ', self.ex, self.ey, 32, 32)
        
    def update(self):
        self.x += self.velocity / 1.5
        self.ex, self.ey = self.x + 15 * -1 * self.velocity, self.y
        self.frame = (self.frame + 5 * game_framework.frame_time) % 3
        
        if self.velocity > 0:
            self.face_dir = 1
        elif self.velocity < 0:
            self.face_dir = -1

        if play_state.player.dir != 0 and self.isFire and\
           play_state.player.x > 400 and play_state.player.x < 1600:
            if play_state.player.isDash == False:
                self.x -= play_state.player.dir * \
                    player_speed.RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x -= play_state.player.dir * 2 * \
                    player_speed.RUN_SPEED_PPS * game_framework.frame_time

        if self.x < 400:
            self.rotate += 0.02
        else:
            self.rotate -= 0.02

    def get_bb(self):
        return self.x - 19, self.y - 19, self.x + 19, self.y + 19

    def handle_collision(self, other, group):
        self.x, self.y, self.velocity = -100, -100, 0
        self.isFire = False
            
