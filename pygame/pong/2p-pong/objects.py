import pygame
import random
import numpy as np
import time
import math

import options


def lerp(a, b, t):
    return a + t * (b - a)


def swept_aabb(prev_center, cur_center, rect):
    dx = cur_center[0] - prev_center[0]
    dy = cur_center[1] - prev_center[1]

    if dx == 0:
        if not (rect.left <= prev_center[0] <= rect.right):
            return None
        tx_enter, tx_exit = -math.inf, math.inf
    else:
        t1 = (rect.left - prev_center[0]) / dx
        t2 = (rect.right - prev_center[0]) / dx
        tx_enter, tx_exit = min(t1, t2), max(t1, t2)

    if dy == 0:
        if not (rect.top <= prev_center[1] <= rect.bottom):
            return None
        ty_enter, ty_exit = -math.inf, math.inf
    else:
        t1 = (rect.top - prev_center[1]) / dy
        t2 = (rect.bottom - prev_center[1]) / dy
        ty_enter, ty_exit = min(t1, t2), max(t1, t2)

    t_enter = max(tx_enter, ty_enter)
    t_exit = min(tx_exit, ty_exit)

    if t_enter > t_exit or t_exit < 0 or t_enter > 1:
        return None
    if t_enter < 0:
        return None

    if tx_enter > ty_enter:
        nx = -1 if dx > 0 else 1
        ny = 0
    else:
        nx = 0
        ny = -1 if dy > 0 else 1

    return t_enter, nx, ny


class Padel():
    def __init__(self, position):
        self.size = (20, 100)
        self.color = (0, 180, 235)
        self.position = position
        self.position[1] = self.position[1] - self.size[1] / 2

        self.move_speed = 270

    def input(self, up, down, delta):
        if up:
            self.position[1] -= self.move_speed * delta
        if down:
            self.position[1] += self.move_speed * delta

    def update(self, up, down, screen, delta):
        self.input(up, down, delta)

        self.rect = pygame.Rect(self.position, self.size)
        self.rect.clamp_ip(screen.get_rect())

        if self.position[1] <= 0:
            self.position[1] = 0
        if self.position[1] >= screen.height:
            self.position[1] = screen.height

        pygame.draw.rect(screen, self.color, self.rect)


padel_l = Padel([options.DISPLAY.get_rect().left + 5,
                options.DISPLAY.get_rect().centery])
padel_r = Padel([options.DISPLAY.get_rect().right -
                padel_l.size[0] - 5, options.DISPLAY.get_rect().centery])


class PadelAI():
    def __init__(self, position):
        self.size = (20, 100)
        self.color = (0, 180, 235)
        self.position = position
        self.position[1] = self.position[1] - self.size[1] / 2

        self.smoothness = 1
        self.move_speed = 270
        self.move_margin = 10

    def update(self, screen, delta, ball_position):
        if ball_position[0] <= self.position[0] - 10:
            position_diff = ball_position[1] - self.position[1]
            max_step = self.move_speed * delta

            if abs(position_diff) >= max_step:
                step = min(self.move_speed * delta, abs(position_diff))
                if position_diff > 0:
                    self.position[1] += step
                else:
                    self.position[1] -= step

            # self.position[1] = ball_position[1]

        self.rect = pygame.Rect(self.position, self.size)
        self.rect.clamp_ip(screen.get_rect())
        pygame.draw.rect(screen, self.color, self.rect)


class Ball():
    def __init__(self, position):
        self.size = (15, 15)
        self.color = (0, 255, 0)
        self.position = position
        self.prev_position = list(position)

        self.speed_vector = [0, 0]
        self.bounces = 0
        self.speed_increment = 20
        self.max_speed = 900

        self.initial_speed = 300

        self.hit_goal = False

        self.point_l = 0
        self.point_r = 0

        self.rect = pygame.Rect(self.position, self.size)

    def increment_speed(self):
        speed = math.hypot(self.speed_vector[0], self.speed_vector[1])
        if speed == 0:
            return
        new_speed = min(speed + self.speed_increment, self.max_speed)
        scale = new_speed / speed
        self.speed_vector[0] *= scale
        self.speed_vector[1] *= scale

    def bounce_screen(self, screen):
        # x
        if self.position[0] <= 0:
            self.hit_goal = True
            self.point_r += 1
        if self.position[0] + self.size[0] >= screen.width:
            self.hit_goal = True
            self.point_l += 1

            if self.position[0] <= 0:
                self.position[0] = 0
            else:
                self.position[0] = screen.width - self.size[0]

        # y
        if self.position[1] <= 0 or self.position[1] + self.size[1] >= screen.height:
            self.increment_speed()

            self.speed_vector[1] *= -1

            self.bounces += 1

            if self.position[1] <= 0:
                self.position[1] = 0
            else:
                self.position[1] = screen.height - self.size[1]

    def bounce_padel(self, padel):
        half_w = self.size[0] / 2
        half_h = self.size[1] / 2

        prev_center = (self.prev_position[0] + half_w,
                       self.prev_position[1] + half_h)
        cur_center = (self.position[0] + half_w,
                      self.position[1] + half_h)

        box = padel.rect.inflate(self.size[0], self.size[1])

        hit = swept_aabb(prev_center, cur_center, box)
        if hit is None:
            return

        t, nx, ny = hit

        contact_x = self.prev_position[0] + \
            (self.position[0] - self.prev_position[0]) * t
        contact_y = self.prev_position[1] + \
            (self.position[1] - self.prev_position[1]) * t

        self.position = [contact_x + nx * 0.5, contact_y + ny * 0.5]

        if nx != 0:
            self.speed_vector[0] *= -1
        if ny != 0:
            self.speed_vector[1] *= -1

        self.increment_speed()

        self.prev_position = list(self.position)
        self.rect = pygame.Rect(self.position, self.size)

    def start_new_round(self, delta, round):
        self.position = [options.DISPLAY.get_rect(
        ).centerx, options.DISPLAY.get_rect().centery]

        time.sleep(0.1)

        side = random.choice([-1, 1])
        # ball_angle = random.uniform(0, 2 * np.pi)
        if side >= 0:
            ball_angle = random.uniform(-1, 1) * 0.1
        else:
            ball_angle = random.uniform(179, 181) * 0.1

        ball_vx = np.cos(ball_angle) * self.initial_speed
        ball_vy = np.sin(ball_angle) * self.initial_speed
        self.speed_vector = [ball_vx, ball_vy]

    def update(self, screen, delta, round):
        self.prev_position = list(self.position)

        self.position[0] += self.speed_vector[0] * delta
        self.position[1] += self.speed_vector[1] * delta

        self.bounce_screen(screen)

        if self.hit_goal:
            self.start_new_round(delta, round)
            self.hit_goal = False
            self.prev_position = list(self.position)

        self.rect = pygame.Rect(self.position, self.size)
        pygame.draw.rect(screen, self.color, self.rect)


ball = Ball([options.DISPLAY.get_rect().centerx,
            options.DISPLAY.get_rect().centery])
