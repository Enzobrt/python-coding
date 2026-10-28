import pygame

SCREEN_SIZE = (600, 400)
DISPLAY = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)

clock = pygame.time.Clock()

FPS = 90
DELTATIME = clock.tick(FPS)/1000
