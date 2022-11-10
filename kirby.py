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
VELOCITY = 60
MASS = 0.005

# 1 : 이벤트 정의
RD, LD, RU, LU, SPACE = range(5)

event_name = ['RD', 'LD', 'RU', 'LU', 'SPACE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
}

# 2 : 상태의 정의


class IDLE:
    @staticmethod
    def enter(self, event):
        print('ENTER IDLE')
        self.dir = 0

    @staticmethod
    def exit(self, event):
        self.prev_state = IDLE
        print('EXIT IDLE')

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 100, 300, 100, 100,
                                           0, ' ', self.x, self.y, 100, 100)
        else:
            self.image.clip_composite_draw(int(self.frame) * 100, 300, 100, 100,
                                           0, 'h', self.x, self.y, 100, 100)


class RUN:
    def enter(self, event):
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
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 100, 100, 100, 100,
                                           0, ' ', self.x, self.y, 100, 100)
        else:
            self.image.clip_composite_draw(int(self.frame) * 100, 100, 100, 100,
                                           0, 'h', self.x, self.y, 100, 100)


class JUMP:
    @staticmethod
    def enter(self, event):
        print('ENTER JUMP')
        self.v = VELOCITY

    @staticmethod
    def exit(self, event):
        print('EXIT JUMP')

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % 8
        
        print(self.dir)

        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        if self.v > 0:
            print(self.v)
            F = (0.5 * self.m * (self.v ** 2))
        else:
            print(self.v)
            F = -(0.5 * self.m * (self.v ** 2))

        self.y += round(F)
        self.v -= 1

        if self.y < 50 :
            self.y = 50
            if self.prev_state == IDLE:
                self.cur_state = IDLE
            if self.prev_state == RUN:
                self.cur_state = RUN
            

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 100, 300, 100, 100,
                                           0, ' ', self.x, self.y, 100, 100)
        else:
            self.image.clip_composite_draw(int(self.frame) * 100, 300, 100, 100,
                                           0, 'h', self.x, self.y, 100, 100)


# 3. 상태 변환 구현
next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, SPACE: JUMP},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE: JUMP},
    JUMP:  {RU: RUN, LU: RUN, RD: RUN, LD: RUN, SPACE: JUMP}
}


class Kirby:
    def __init__(self):
        self.x, self.y = 800 // 2, 50
        self.v, self.m = VELOCITY, MASS
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('animation_sheet.png')
        # self.timer = 100
        self.event_que = []
        self.cur_state = IDLE
        self.prev_state = None
        self.cur_state.enter(self, None)
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

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
