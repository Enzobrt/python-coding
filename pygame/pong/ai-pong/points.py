import pygame

from options import DISPLAY


class Score():
    def __init__(self, position):
        self.size = (20, 100)
        self.color = (255, 255, 255)
        self.position = position

    def update(self, screen, font, score):
        self.text_rect = font.render(str(score), True, self.color)

        screen.blit(self.text_rect, self.position)


score_l = Score([DISPLAY.get_rect().centerx - 50, DISPLAY.get_rect().top])
score_r = Score([DISPLAY.get_rect().centerx + 50, DISPLAY.get_rect().top])
