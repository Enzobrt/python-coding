import pygame

pygame.init()

SCREEN_SIZE = (600, 400)
DISPLAY = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)

clock = pygame.time.Clock()

FPS = 90
DELTATIME = clock.tick(FPS)/1000

font = pygame.font.SysFont("notosansmono", 36)
# print(pygame.font.get_fonts())
