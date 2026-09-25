import pygame
import socket

pygame.init()

SCREEN_SIZE = (800, 600)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

SCREEN_CENTERX, SCREEN_CENTERY = SCREEN.get_width() / 2, SCREEN.get_height() / 2

pygame.display.set_caption("Multiplayer test")

BACKGROUND_COLOR = (255, 255, 255)

MOUSE_POS = pygame.mouse.get_pos()


def draw_rect(surface, color, rect):
    pygame.draw.rect(surface, color, rect)


def draw_grid():
    pass


class tic_tac_toc:
    def __init__(self):
        draw_grid()


tic_tac_toc = tic_tac_toc()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("Click", MOUSE_POS)

    MOUSE_POS = pygame.mouse.get_pos()

    SCREEN.fill(BACKGROUND_COLOR)

    draw_grid()

    pygame.display.flip()

pygame.quit()
