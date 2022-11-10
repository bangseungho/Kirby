from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
VELOCITY = 150
MASS = 0.005

# 1 : 이벤트 정의
RD, LD, RU, LU = range(4)

event_name = ['RD', 'LD', 'RU', 'LU']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
}

# 2 : 상태의 정의

def set_speed(time_per_action, frames_per_action):
    global FRAMES_PER_ACTION
    global TIME_PER_ACTION
    global ACTION_PER_TIME
    TIME_PER_ACTION = time_per_action
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = frames_per_action

class IDLE:
    @staticmethod
    def enter(self, event):
        set_speed(1, 6)
        print('ENTER IDLE')
        self.dir = 0

    @staticmethod
    def exit(self, event):
        self.prev_state = IDLE
        print('EXIT IDLE')

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % 6
        self.jump()

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 22, 0, 22, 20,
                                           0, ' ', self.x, self.y, 44, 40)
        else:
            self.image.clip_composite_draw(int(self.frame) * 22, 0, 22, 20,
                                           0, 'h', self.x, self.y, 44, 40)


class RUN:
    def enter(self, event):
        set_speed(0.5, 6)
        print('ENTER RUN')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event):
        self.prev_state = RUN
        self.face_dir = self.dir
        print('EXIT RUN')

    def do(self):
        self.face_dir = self.dir
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % 8
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        self.jump()

        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 23, 186, 23, 21,
                                           0, ' ', self.x, self.y, 46, 42)
        else:
            self.image.clip_composite_draw(int(self.frame) * 23, 186, 23, 21,
                                           0, 'h', self.x, self.y, 46, 42)
  
# 3. 상태 변환 구현
next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE},
}


class Kirby:
    def __init__(self):
        self.x, self.y = 800 // 2, 50
        self.v, self.m = VELOCITY, MASS
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('resource/Default_Kirby.png')
        # self.timer = 100
        self.event_que = []
        self.cur_state = IDLE
        self.prev_state = None
        self.cur_state.enter(self, None)
        self.isJump = 0

    def update(self):
        self.cur_state.do(self)
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                # 에러가 발생했으면, 그때 상태와 이벤트를 출력해본다.
                print(self.cur_state, event_name[event])
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        debug_print('pppp')
        debug_print(f'Face Dir: {self.face_dir}, Dir: {self.dir}')

    def add_event(self, event):
        self.event_que.insert(0, event)

    def jump(self):
        if self.isJump == 1:
            if self.v > 0:
                F = ( (RUN_SPEED_PPS * game_framework.frame_time / 20) * self.m * (self.v ** 2))
            else:
                F = -((RUN_SPEED_PPS * game_framework.frame_time / 40) * self.m * (self.v ** 2))

            self.y += round(F)
            self.v -= 1

            if self.y < 50:
                self.y = 50
                self.v = VELOCITY
                self.isJump = 0

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if not self.isJump:
                self.isJump = 1
            elif self.isJump == 1:
                self.isJump = 2