from pico2d import *
from star import Star
from breath import Breath
from enum import Enum
from player_speed import *
import play_state
import game_world
import game_framework

LEFT = 0
BOTTOM = 1
RIGHT = 2
TOP = 3

# 1 : 이벤트 정의
RD, LD, RU, LU, TIMER, CD, CU = range(7)

event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'CD', 'CU']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_LCTRL): CD,
    (SDL_KEYUP, SDLK_LCTRL): CU,
}

# 2 : 상태의 정의


class IDLE:
    @staticmethod
    def enter(self, event):
        global PREV
        PREV = IDLE
        print('ENTER IDLE')
        self.dir = 0
        self.timer = 40

    @staticmethod
    def exit(self, event):
        self.prev_event = self.face_dir
        if self.isBite == 1 and event == CD:
            self.fire_star()
            self.isBite = 2
        print('EXIT IDLE')

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.jump()
        self.timer -= 1

    @staticmethod
    def draw(self):
        if self.isJump == 0:  # 기본 상태
            if self.isBite == True:
                self.set_speed(1, 6)
                self.set_image(25, 22, 312)
            if self.isBite == False:
                self.set_speed(1, 6)
                self.set_image(26, 20, 0)
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466)
                if self.frame > 4:
                    self.isBite = False
        elif self.isJump == 1:  # 점프 상태
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466)
                if self.frame > 4:
                    self.isBite = False
            elif self.isDrop != 0:
                self.set_speed(1.5, 18)
                self.set_image(27, 24, 138)

            else:
                if self.isBite:
                    if self.frame > 5:
                        self.frame = 5
                    self.set_speed(0.8, 5)
                    self.set_image(31, 29, 408)
                else:
                    if self.v > 0:
                        self.frame = 0
                    if self.frame > 8:
                        self.frame = 8
                    self.set_speed(0.45, 10)
                    self.set_image(27, 22, 40)
        else:  # 나는 상태
            if int(self.frame) == 12:
                self.frame = 5
            self.set_speed(1.2, 13)
            self.set_image(28, 27, 84)
        self.composite_draw()


PREV = IDLE


class RUN:
    def enter(self, event):
        global PREV
        PREV = RUN
        self.set_speed(0.5, 8)
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
        self.face_dir = self.dir
        self.prev_event = self.face_dir
        if self.isBite == 1 and event == CD:
            self.fire_star()
            self.isBite = 2
        print('EXIT RUN')

    def do(self):
        self.can_move = True
        self.face_dir = self.dir
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        if self.x < 400 or self.x >= 1600:
            self.screen_x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        if self.timer > 0 and self.isBite == False and self.face_dir == self.prev_event:
            self.add_event(TIMER)

        print("POS_X : ", self.x)
        print("SCREEN_X : ", self.screen_x)
    
        self.jump()

    def draw(self):
        if self.isJump == 0:
            if self.isBite == True:
                self.set_speed(0.7, 16)
                self.set_image(26, 26, 356)
            if self.isBite == False:
                self.set_speed(0.7, 8)
                self.set_image(26, 21, 186)
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466)
                if self.frame > 4:
                    self.isBite = False
        elif self.isJump == 1:  # 점프 상태
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466)
                if self.frame > 4:
                    self.isBite = False
            elif self.isDrop != 0:
                self.set_speed(1.5, 18)
                self.set_image(27, 24, 138)

            else:
                if self.isBite:
                    if self.frame > 5:
                        self.frame = 5
                    self.set_speed(0.8, 5)
                    self.set_image(31, 29, 408)
                else:
                    if self.v > 0:
                        self.frame = 0
                    if self.frame > 8:
                        self.frame = 8
                    self.set_speed(0.45, 10)
                    self.set_image(27, 22, 40)
        else:  # 나는 상태
            if int(self.frame) == 12:
                self.frame = 5
            self.set_speed(1.2, 13)
            self.set_image(28, 27, 84)
        self.composite_draw()


class DASH:
    def enter(self, event):
        self.set_speed(0.5, 8)
        print('ENTER DASH')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event):
        self.face_dir = self.dir
        self.isDash = False
        print('EXIT DASH')

    def do(self):
        self.can_move = True
        self.face_dir = self.dir
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
                      
        if self.isJump == 2 or self.isDrop:
            self.isDash = False
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        else:
            self.isDash = True
            self.x += self.dir * RUN_SPEED_PPS * 2 * game_framework.frame_time
            

        if self.x < 400 or self.x >= 1600:
            self.screen_x += self.dir * RUN_SPEED_PPS * 2 * game_framework.frame_time

        print("POS_X : ", self.x)
        print("SCREEN_X : ", self.screen_x)
        
        self.jump()

    def draw(self):
        if self.isJump == 0:
            self.set_speed(0.7, 8)
            self.set_image(26, 21, 228)
        elif self.isJump == 1:  # 점프 상태
            if self.isDrop != 0:
                self.set_speed(1.5, 18)
                self.set_image(27, 24, 138)
            else:
                if self.v > 0:
                    self.frame = 0
                if self.frame > 8:
                    self.frame = 8
                self.set_speed(0.45, 10)
                self.set_image(27, 22, 40)
        else:  # 나는 상태
            if int(self.frame) == 12:
                self.frame = 5
            self.set_speed(1.2, 13)
            self.set_image(28, 27, 84)
        self.composite_draw()


class SUCK:
    range = [0, 0, 0, 0]

    @staticmethod
    def enter(self, event):
        self.set_speed(0.6, 5)
        self.frame = 0
        self.dir = 0
        print('ENTER SUCK')

    @staticmethod
    def exit(self, event):
        if PREV == IDLE:
            self.cur_state = IDLE
        elif PREV == RUN:
            if self.face_dir == 1:
                self.dir += 1
            else:
                self.dir -= 1
            self.cur_state = RUN
        pass

        print('EXIT SUCK')

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time)
        SUCK.range = [self.screen_x - 50 + 50 * self.face_dir, self.y -
                      22, self.screen_x + 50 + 50 * self.face_dir, self.y + 22]
        self.jump()

    @staticmethod
    def draw(self):
        if int(self.frame) == 5:
            self.frame = 2
        self.set_image(25, 22, 270)
        draw_rectangle(SUCK.range[LEFT], SUCK.range[BOTTOM],
                       SUCK.range[RIGHT], SUCK.range[TOP])
        self.composite_draw()


# 3. 상태 변환 구현
next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, CD: SUCK, CU: IDLE},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, TIMER: DASH, CD: SUCK, CU: RUN},
    DASH:  {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, CD: SUCK},
    SUCK:  {RU: IDLE, LU: IDLE, RD: RUN, LD: RUN}
}

class Kirby:
    def __init__(self):
        self.x, self.y = 800 // 2, 90
        self.screen_x, self.screen_y = 800// 2, 90
        self.v, self.m = VELOCITY, MASS
        self.w, self.h = 22, 20
        self.image_posY = None
        self.frame = 0
        self.dir, self.diry, self.face_dir = 0, 0, 1
        self.image = load_image('resource/Default_Kirby.png')
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)
        self.prev_event = None
        self.isJump = 0
        self.isDrop = 0
        self.isBite = 0
        self.isDash = 0
        self.timer = 0
        self.can_move = True
        self.cur_floor_posY = 90
        
    def update(self):
        self.gravity()
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
        draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_floor(self, other):
        if self.screen_x > other.x-other.w and self.screen_x < other.x + other.w:
            self.cur_floor_posY = other.y + other.h + self.h
        print(self.cur_floor_posY)

    def gravity(self):
        if self.v <= 0:
            F = -((RUN_SPEED_PPS * game_framework. frame_time)
                    * self.m * (self.v ** 2)) / 100
            self.y += round(F)
            self.v -= 1
            
    def jump(self):
        if self.isJump == 1:
            if self.v > 0:
                F = ((RUN_SPEED_PPS * game_framework.frame_time)
                     * self.m * (self.v ** 2)) / 30
                self.y += round(F)
                self.v -= 1
                
            if self.isDrop == 2 and self.y < self.cur_floor_posY:
                self.y = self.cur_floor_posY
                self.v = VELOCITY - 30
                self.isJump = 1
                self.isDrop = 1

            if self.y < self.cur_floor_posY:
                if self.isDrop == 1:
                    self.isDrop = 0
                self.y = self.cur_floor_posY
                self.v = VELOCITY
                self.isJump = 0

        elif self.isJump == 2:
            self.v = 0
            self.y -= GRAVITY * game_framework.frame_time
            self.y += self.diry * RUN_SPEED_PPS * game_framework.frame_time
            self.y = clamp(90, self.y, 425)
        

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                if self.isJump == 0:
                    self.isJump = 1
                elif self.isJump == 1 and self.isBite == False:
                    self.isJump = 2
            if event.key == SDLK_UP:
                self.diry += 1
            if event.key == SDLK_DOWN:
                self.diry -= 1
            if event.key == SDLK_SPACE:
                self.frame = 0
            if event.key == SDLK_b:
                if self.isBite == False:
                    self.isBite = True
                else:
                    self.isBite = False
        if event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                self.diry -= 1
            if event.key == SDLK_DOWN:
                self.diry += 1
            if event.key == SDLK_SPACE:
                if self.isJump == 2:
                    self.fire_breath()
                    self.isJump = 1
                    self.isDrop = 2
                    self.frame = 0

    def set_speed(self, time_per_action, frames_per_action):
        global FRAMES_PER_ACTION
        global TIME_PER_ACTION
        global ACTION_PER_TIME
        TIME_PER_ACTION = time_per_action
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = frames_per_action

    def composite_draw(self):
        if self.face_dir == 1:
            self.image.clip_composite_draw(int(
                self.frame) * self.w, self.image_posY, self.w, self.h, 0, ' ', self.screen_x, self.y, self.w * 2, self.h * 2)
        else:
            self.image.clip_composite_draw(int(
                self.frame) * self.w, self.image_posY, self.w, self.h, 0, 'h', self.screen_x, self.y, self.w * 2, self.h * 2)

    def set_image(self, width, height, image_posY):
        self.w = width
        self.h = height
        self.image_posY = image_posY

    def fire_star(self):
        star = Star(self.screen_x, self.y, self.face_dir*2)
        game_world.add_object(star, 1)
        game_world.add_collision_pairs(star, play_state.stage.cur_state.obstacle, 'star:ob')

    def fire_breath(self):
        breath = Breath(self.screen_x, self.y, self.face_dir*2, self.face_dir)
        game_world.add_object(breath, 1)

    def get_bb(self):
        return self.screen_x - self.w, self.y - self.h, \
                self.screen_x + self.w, self.y + self.h
    
    def handle_collision(self, other, group):
        if group == 'player:ob':
            if self.dir == 1 and self.face_dir == 1:
                if self.x < other.px and self.y < other.py + other.h + self.h:
                    self.screen_x = other.x - other.w - self.w
                    self.x = other.px - other.w - self.w
                    self.can_move = False
            elif self.dir == -1 and self.face_dir == -1:
                if self.x > other.px and self.y < other.py + other.h + self.h:
                    self.screen_x = other.x + other.w + self.w
                    self.x = other.px + other.w + self.w
                    self.can_move = False
            self.get_floor(other)