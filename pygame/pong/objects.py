import pygame
import random
import numpy as np

import options


def lerp(a, b, t):
    return a + t * (b - a)


class Padel():
    def __init__(self, position):
        self.size = (20, 100)
        self.color = (255, 255, 255)
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


padel_l = Padel([options.DISPLAY.get_rect().left + 20,
                options.DISPLAY.get_rect().centery])
# padel_r = Padel([options.DISPLAY.get_rect().right - padel_l.size[0], options.DISPLAY.get_rect().centery])


class PadelAI():
    def __init__(self, position):
        self.size = (20, 100)
        self.color = (255, 255, 255)
        self.position = position
        self.position[1] = self.position[1] - self.size[1] / 2

        self.smoothness = 1
        self.move_speed = 270

    def update(self, screen, delta, ball_position):
        self.rect = pygame.Rect(self.position, self.size)
        self.rect.clamp_ip(screen.get_rect())

        if self.position[1] <= 0:
            self.position[1] = 0
        if self.position[1] >= screen.height:
            self.position[1] = screen.height

        if ball_position[0] <= self.position[0] - 10:
            self.position[1] = lerp(
                self.position[1], ball_position[1], self.smoothness)

        pygame.draw.rect(screen, self.color, self.rect)


padel_ai = PadelAI([options.DISPLAY.get_rect().right - padel_l.size[0] * 2, options.DISPLAY.get_rect().centery])


class Ball():
    def __init__(self, position):
        self.size = (15, 15)
        self.color = (0, 255, 0)
        self.position = position

        self.speed_vector = [0, 0]
        self.bounces = 0
        self.speed_increment = 60

        self.initial_speed = 300

        self.hit_goal = False

    def bounce_screen(self, screen):
        # x
        if self.position[0] <= 0 or self.position[0] + self.size[0] >= screen.width:
            # self.speed_vector[0] *= -1
            self.hit_goal = True

            if self.position[0] <= 0:
                self.position[0] = 0
            else:
                self.position[0] = screen.width - self.size[0]

        # y
        if self.position[1] <= 0 or self.position[1] + self.size[1] >= screen.height:
            self.speed_vector[0] += self.speed_increment
            self.speed_vector[1] += self.speed_increment

            self.speed_vector[1] *= -1

            self.bounces += 1
            print(self.bounces)

            if self.position[1] <= 0:
                self.position[1] = 0
            else:
                self.position[1] = screen.height - self.size[1]

    def bounce_padel(self, padel):
        if self.rect.colliderect(padel):
            self.speed_vector[0] += self.speed_increment
            self.speed_vector[1] += self.speed_increment

            self.speed_vector[0] *= -1


    def start_new_round(self, delta, round):
        self.position = [options.DISPLAY.get_rect(
        ).centerx, options.DISPLAY.get_rect().centery]

        ball_angle = random.uniform(0, 2 * np.pi)

        ball_vx = np.cos(ball_angle) * self.initial_speed
        ball_vy = np.sin(ball_angle) * self.initial_speed
        self.speed_vector = [ball_vx, ball_vy]

    def update(self, screen, delta, round):
        self.position[0] += self.speed_vector[0] * delta
        self.position[1] += self.speed_vector[1] * delta

        self.rect = pygame.Rect(self.position, self.size)

        self.bounce_screen(screen)

        if self.hit_goal:
            self.start_new_round(delta, round)
            self.hit_goal = False

        pygame.draw.rect(screen, self.color, self.rect)


ball = Ball([options.DISPLAY.get_rect().centerx,
            options.DISPLAY.get_rect().centery])
