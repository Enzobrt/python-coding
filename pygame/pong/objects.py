import pygame

import options


class Padel():
    def __init__(self, position):
        self.size = (20, 100)
        self.color = (255, 255, 255)
        self.position = position
        self.position[1] = self.position[1] - self.size[1] / 2

        self.move_speed = 100

    def input(self, up, down, delta):
        if up:
            self.position[1] -= self.move_speed * delta
        if down:
            self.position[1] += self.move_speed * delta

    def update(self, up, down, screen, delta):
        self.input(up, down, delta)

        self.rect = pygame.Rect(self.position, self.size)
        pygame.draw.rect(screen, self.color, self.rect)


padel_l = Padel([options.DISPLAY.get_rect().left,
                options.DISPLAY.get_rect().centery])
padel_r = Padel([options.DISPLAY.get_rect().right -
                padel_l.size[0], options.DISPLAY.get_rect().centery])


class Ball():
    def __init__(self, position):
        self.size = (15, 15)
        self.color = (0, 255, 0)
        self.position = position

        self.speed_vector = [0, 0]

    def update(self, screen, delta):
        self.position[0] += self.speed_vector[0] * delta
        self.position[1] += self.speed_vector[1] * delta

        self.rect = pygame.Rect(self.position, self.size)
        pygame.draw.rect(screen, self.color, self.rect)


ball = Ball([options.DISPLAY.get_rect().centerx,
            options.DISPLAY.get_rect().centery])
