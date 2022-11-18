from pico2d import *
from star import Star
from breath import Breath
from enum import Enum
from player_speed import *
import play_state
import game_world
from spark import DAMAGED
import game_framework
from spark import ATTACK
from spark import SUCKED
from spark import PULL
from spark import TURN
import time

LEFT = 0
BOTTOM = 1
RIGHT = 2
TOP = 3

class Ability(Enum):
    Defualt = 0,
    Spark = 1,
    Laser = 2,
    Fire = 3

# 1 : 이벤트 정의
RD, LD, RU, LU, TIMER, CD, CU, BITE, TRANS, AATTACK = range(10)

event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'CD', 'CU', 'BITE', 'TRANS', 'AATTACK']

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
                self.set_image(22, 22, 312, 3, 0)
            if self.isBite == False:
                self.set_speed(1, 6)
                self.set_image(26, 20, 0, 0, 14)
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466, 0, 0)
                if self.frame > 4:
                    self.isBite = False
        elif self.isJump == 1:  # 점프 상태
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466, 0, 0)
                if self.frame > 4:
                    self.isBite = False
            elif self.isDrop != 0:
                self.set_speed(1.5, 18)
                self.set_image(27, 24, 138, 0, 20)

            else:
                if self.isBite:
                    if self.frame > 5:
                        self.frame = 5
                    self.set_speed(0.8, 5)
                    self.set_image(24, 25, 408, 7, 2)
                else:
                    if self.v > 0:
                        self.frame = 0
                    if self.frame > 8:
                        self.frame = 8
                    self.set_speed(0.45, 10)
                    self.set_image(26, 22, 40, 1, 20)
        else:  # 나는 상태
            if int(self.frame) == 12:
                self.frame = 5
            self.set_speed(1.2, 13)
            self.set_image(28, 27, 84, 0, 15)
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
        self.face_dir = self.dir

    def exit(self, event):
        self.prev_event = self.face_dir
        if self.isBite == 1 and event == CD:
            self.fire_star()
            self.isBite = 2
        print('EXIT RUN')

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        if self.x < 400 or self.x >= 1600:
            self.screen_x += self.dir * RUN_SPEED_PPS * game_framework.frame_time

        if not self.isCollide:
            self.dir = self.face_dir

        if self.timer > 0 and self.isBite == False and self.face_dir == self.prev_event:
            self.add_event(TIMER)
        self.jump()

    def draw(self):
        if self.isJump == 0:
            if self.isBite == True:
                self.set_speed(0.7, 16)
                self.set_image(22, 22, 356, 4, 4)
            if self.isBite == False:
                self.set_speed(0.7, 8)
                self.set_image(26, 21, 186, 0, 20)  # 바꿈
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466, 0, 0)
                if self.frame > 4:
                    self.isBite = False
        elif self.isJump == 1:  # 점프 상태
            if self.isBite == 2:
                self.set_speed(0.3, 5)
                self.set_image(24, 22, 466, 0, 0)
                if self.frame > 4:
                    self.isBite = False
            elif self.isDrop != 0:
                self.set_speed(1.5, 18)
                self.set_image(27, 24, 138, 0, 20)  # 바꿈
            else:
                if self.isBite:
                    if self.frame > 5:
                        self.frame = 5
                    self.set_speed(0.8, 5)
                    self.set_image(24, 25, 408, 7, 2)  # 바꿀거
                else:
                    if self.v > 0:
                        self.frame = 0
                    if self.frame > 8:
                        self.frame = 8
                    self.set_speed(0.45, 10)
                    self.set_image(27, 22, 40, 0, 20)  # 바꿈
        else:  # 나는 상태
            if int(self.frame) == 12:
                self.frame = 5
            self.set_speed(1.2, 13)
            self.set_image(28, 27, 84, 0, 15)
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
        self.face_dir = self.dir

    def exit(self, event):
        self.isDash = False
        print('EXIT DASH')

    def do(self):
        self.can_move = True
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

        if not self.isCollide:
            self.dir = self.face_dir

        self.jump()

    def draw(self):
        if self.isJump == 0:
            self.set_speed(0.7, 8)
            self.set_image(26, 22, 228, 31, 9)  # 바꿈
        elif self.isJump == 1:  # 점프 상태
            if self.isDrop != 0:
                self.set_speed(1.5, 18)
                self.set_image(27, 24, 138, 0, 20)
            else:
                if self.v > 0:
                    self.frame = 0
                if self.frame > 8:
                    self.frame = 8
                self.set_speed(0.45, 10)
                self.set_image(26, 22, 40, 1, 20)
        else:  # 나는 상태
            if int(self.frame) == 12:
                self.frame = 5
            self.set_speed(1.2, 13)
            self.set_image(28, 27, 84, 0, 15)
        self.composite_draw()


class SUCK:
    range = [0, 0, 0, 0]

    @staticmethod
    def enter(self, event):
        print('ENTER SUCK')
        if self.ability != Ability.Defualt:
            self.add_event(AATTACK)
        self.set_speed(0.3, 5)
        self.frame = 0
        self.dir = 0

    @staticmethod
    def exit(self, event):
        if self.ability == Ability.Defualt:
            if PREV == IDLE:
                self.cur_state = IDLE
            elif PREV == RUN:
                if self.face_dir == 1:
                    self.dir += 1
                else:
                    self.dir -= 1
                self.cur_state = RUN
            for enemy in play_state.stage.enemys:
                if enemy.cur_state == PULL:
                    enemy.add_event(TURN)
            self.timer = 0
        print('EXIT SUCK')

    @staticmethod
    def do(self):
        if self.ability == Ability.Defualt:
            self.frame = (self.frame + FRAMES_PER_ACTION *
                        ACTION_PER_TIME * game_framework.frame_time)
            SUCK.range = [self.screen_x - 50 + 50 * self.face_dir, self.y -
                        22, self.screen_x + 50 + 50 * self.face_dir, self.y + 22]

            for enemy in play_state.stage.enemys:
                if SUCK.range[RIGHT] > enemy.x - enemy.w and \
                SUCK.range[LEFT] < enemy.x + enemy.w and \
                SUCK.range[TOP] > enemy.y - enemy.h and \
                SUCK.range[BOTTOM] < enemy.y + enemy.h:

                    enemy.add_event(SUCKED)

                    if enemy.dis_to_player <= 5:
                        self.bite_enemy_type = enemy.type
                        enemy.death_timer = 1
                        enemy.add_event(DAMAGED)
                        enemy.x = -10000
                        self.isBite = True
                        self.add_event(BITE)

            self.jump()
    @staticmethod
    def draw(self):
        if int(self.frame) == 5:
            self.frame = 2
        self.set_image(25, 22, 270, 0, 0)
        draw_rectangle(SUCK.range[LEFT], SUCK.range[BOTTOM],
                       SUCK.range[RIGHT], SUCK.range[TOP])
        self.composite_draw()


class TRANSFORM:
    @staticmethod
    def enter(self, event):
        print('ENTER TRANSFORM')
        self.effect = load_image('resource/trans_effect.png')
        self.frame = 0
        self.effect_frame = 0
        self.dir = 0

    @staticmethod
    def exit(self, event):
        print('EXIT TRANSFORM')
        print(self.bite_enemy_type)
        match(self.bite_enemy_type):
            case 2:
                self.ability = Ability.Spark
                self.image = load_image('resource/Spark_Kirby.png')
            case 3:
                self.ability = Ability.Laser
                self.image = load_image('resource/Laser_Kirby.png')
            case 4:
                self.ability = Ability.Fire
                self.image = load_image('resource/Fire_Kirby.png')
        self.bite_enemy_type = None
                
    @staticmethod
    def do(self):
        self.set_speed(1.0, 16)
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        
        self.set_speed(0.6, 16)
        self.effect_frame = (self.effect_frame + FRAMES_PER_ACTION *
                             ACTION_PER_TIME * game_framework.frame_time)

        if int(self.effect_frame) == 16:
            self.add_event(TIMER)

    @staticmethod
    def draw(self):
        self.set_image(32, 22, 510, 0, 0)
        self.composite_draw()

        self.set_image(80, 80, 0, 0, 0)
        self.ecomposite_draw(self.effect)

class ABILITY:
    @staticmethod
    def enter(self, event):
        print('ENTER ABILITY')
        self.v = 1
        match(self.ability):
            case Ability.Spark:
                self.set_speed(0.5, 11)
                self.set_image(64, 74, 258, 0, 0)
            case Ability.Laser:
                pass
            case Ability.Fire:
                pass

        self.frame = 0

    @staticmethod
    def exit(self, event):
        self.v = 150
        if PREV == RUN:
            if event == RD:
                self.dir += 1
            elif event == LD:
                self.dir -= 1
            elif event == CU:
                if self.face_dir == 1:
                    self.dir = 1
                else:
                    self.dir = -1
            self.cur_state = RUN
            self.timer = 0
        print('EXIT ABILITY')
       
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION *
                      ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if int(self.frame) == 10:
            self.frame = 1
        
    @staticmethod
    def draw(self):
        self.composite_draw()
        pass



# 3. 상태 변환 구현
next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, CD: SUCK, CU: IDLE, BITE: IDLE, TRANS: TRANSFORM},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, TIMER: DASH, CD: SUCK, CU: RUN, TRANS: TRANSFORM},
    DASH:  {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, CD: SUCK, TRANS: TRANSFORM},
    SUCK:  {AATTACK: ABILITY, RU: IDLE, LU: IDLE, RD: RUN, LD: RUN, BITE: IDLE},
    TRANSFORM: {TIMER: IDLE},
    ABILITY: {CU: IDLE, RU: IDLE, LU: IDLE, RD: RUN, LD: RUN,}
}


class Kirby:
    def __init__(self):
        self.x, self.y = 800 // 2, 90
        self.screen_x, self.screen_y = 800 // 2, 90
        self.v, self.m = VELOCITY, MASS
        self.w, self.h, self.tw, self.th = 22, 20, 0, 0
        self.image_posY = None
        self.frame = 0
        self.dir, self.diry, self.face_dir = 0, 0, 1
        self.ability = Ability.Defualt
        self.image = load_image('resource/Default_Kirby.png')
        #----------------------------------------------------
        self.Life = load_image("resource/life_hud.png")
        self.Life_0 = load_image("resource/0_hud.png")
        self.Life_1 = load_image("resource/1_hud.png")
        self.Life_2 = load_image("resource/2_hud.png")
        self.Life_x = load_image("resource/x_hud.png")
        self.Hp = load_image("resource/hp_hud.png")
        self.lifes = 2
        self.hps = 6
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_end_time = 0
        self.cnt = 0
        #----------------------------------------------------
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)
        self.prev_event = None
        self.isJump = 0
        self.isDrop = 0
        self.isBite = 0
        self.isDash = 0
        self.timer = 0
        self.can_move = 1
        self.cur_floor = 90
        self.can_jump = False
        self.isCollide = 0
        self.star = []
        self.type = 1
        self.bite_enemy_type = None

    def update(self):
        self.gravity()
        self.cur_state.do(self)
        self.invincible_end_time = time.time()
        if self.invincible_end_time - self.invincible_start_time >= 3:
            self.invincible = False

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

        self.Life.draw(40, 420, 32, 25)

        self.Life_x.draw(69, 419, 15.5, 16)

        if self.lifes == 2:
            self.Life_0.draw(90, 420, 16, 22)
            self.Life_2.draw(106, 420, 16, 22)
        if self.lifes == 1:
            self.Life_0.draw(90, 420, 16, 22)
            self.Life_1.draw(106, 420, 16, 22)
        if self.lifes == 0:
            self.Life_0.draw(90, 420, 16, 22)
            self.Life_0.draw(106, 420, 16, 22)

        for hp in range(self.hps):
            self.Hp.draw(130 + hp * 18, 420, 18, 29.5)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def gravity(self):
        if self.v <= 0:
            F = -((RUN_SPEED_PPS * game_framework.frame_time)
                  * self.m * (self.v ** 2)) / 100
            self.y += round(F)
            self.v -= 1

        elif self.y > self.cur_floor:
            F = -((RUN_SPEED_PPS * game_framework.frame_time)
                  * self.m * (self.v ** 2)) / 100
            self.y += round(F)

            if self.y < self.cur_floor:
                self.y = self.cur_floor

    def jump(self):
        if self.isJump == 1:
            if self.v > 0:
                F = ((RUN_SPEED_PPS * JUMP_HEIGHT)
                     * self.m * (self.v ** 2)) / 25
                self.y += round(F)
                self.v -= 1

            if self.isDrop == 2 and self.y < self.cur_floor:
                self.y = self.cur_floor
                self.v = VELOCITY - 30
                self.isJump = 1
                self.isDrop = 1

            if self.y < self.cur_floor:
                if self.isDrop == 1:
                    self.isDrop = 0
                self.v = VELOCITY
                self.isJump = 0

        elif self.isJump == 2:
            self.v = 0
            self.y -= GRAVITY * game_framework.frame_time
            self.y += self.diry * RUN_SPEED_PPS * game_framework.frame_time
            self.y = clamp(self.cur_floor, self.y, 425)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                self.can_jump = True
                if self.isJump == 0:
                    self.isJump = 1
                elif self.isJump == 1 and self.isBite == False:
                    self.isJump = 2
            if event.key == SDLK_UP:
                self.diry += 1
            if event.key == SDLK_DOWN:
                if self.cur_state == IDLE:
                    if self.isBite == 1:
                        self.add_event(TRANS)
                    self.isBite = False
                self.diry -= 1
            if event.key == SDLK_BACKSPACE:
                self.ability = Ability.Defualt
                self.image = load_image('resource/Default_Kirby.png')
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

    def set_image(self, width, height, image_posY, trans_width, trans_height):
        self.w = width
        self.h = height
        self.tw = trans_width
        self.th = trans_height
        self.image_posY = image_posY

    def composite_draw(self):
        self.cnt += 1
        if self.invincible:
            if self.cnt % 2 == 0:
                if self.face_dir == 1:
                    self.image.clip_composite_draw(int(
                        self.frame) * (self.w + self.tw), self.image_posY, self.w + self.tw, self.h + self.th, 0, ' ', self.screen_x - self.tw / 2, self.y + self.th + 5, (self.w + self.tw) * 2, (self.h + self.th) * 2)
                else:
                    self.image.clip_composite_draw(int(
                        self.frame) * (self.w + self.tw), self.image_posY, self.w + self.tw, self.h + self.th, 0, 'h', self.screen_x + self.tw / 2, self.y + self.th + 5, (self.w + self.tw) * 2, (self.h + self.th) * 2)
        elif not self.invincible:
            if self.face_dir == 1:
                self.image.clip_composite_draw(int(
                    self.frame) * (self.w + self.tw), self.image_posY, self.w + self.tw, self.h + self.th, 0, ' ', self.screen_x - self.tw / 2, self.y + self.th + 5, (self.w + self.tw) * 2, (self.h + self.th) * 2)
            else:
                self.image.clip_composite_draw(int(
                    self.frame) * (self.w + self.tw), self.image_posY, self.w + self.tw, self.h + self.th, 0, 'h', self.screen_x + self.tw / 2, self.y + self.th + 5, (self.w + self.tw) * 2, (self.h + self.th) * 2)

    def ecomposite_draw(self, who):
        who.clip_composite_draw(int(
            self.effect_frame) * (self.w + self.tw), self.image_posY, self.w + self.tw, self.h + self.th, 0, ' ', self.screen_x - self.tw / 2, self.y + self.th + 20, (self.w + self.tw) * 1.5, (self.h + self.th) * 1.5)

    def damaged(self, damage):

        if not self.invincible:
            self.invincible_start_time = time.time()
            self.invincible = True
            self.hps -= damage
            if self.hps <= 0:
                self.lifes -= 1
                self.hps = 6

    def fire_star(self):
        play_state.star.x = self.screen_x
        play_state.star.y = self.y
        play_state.star.velocity = self.face_dir*2
        play_state.star.isFire = True

    def fire_breath(self):
        breath = Breath(self.screen_x, self.y, self.face_dir*2, self.face_dir)
        game_world.add_object(breath, 1)

    def get_bb(self):
        if self.cur_state == ABILITY:
            return self.screen_x - 60, self.y -60, self.screen_x + 60, self.y + 60
        return self.screen_x - 20, self.y - 20, \
            self.screen_x + 20, self.y + 20
    def handle_collision(self, other, group):
        if group == 'player:ob':
            if self.dir == 1 and self.face_dir == 1 and self.screen_x < other.x and \
                    self.y < other.y + other.h + 20:
                self.dir -= 1
                self.isCollide = True
                self.face_dir = 1
            if self.dir == -1 and self.face_dir == -1 and self.screen_x > other.x and \
                    self.y < other.y + other.h + 20:
                self.dir += 1
                self.isCollide = True
                self.face_dir = -1
        if group == 'player:enemy':
            if self.cur_state != SUCK:
                if self.cur_state != ABILITY:
                    if other.cur_state == ATTACK:
                        if int(other.frame) == 10:
                            self.damaged(3)
                    else:
                        self.damaged(1)
            
