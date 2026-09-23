import pygame
import socket

pygame.init()

SCREEN_SIZE = (800, 800)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Multiplayer test")

BACKGROUND_COLOR = (255, 255, 255)

MOUSE_POS = pygame.mouse.get_pos()


class tic_tac_toc:
    def __init__(self):
        self.draw_grid()

    def draw_rect(surface, pos, size, color):
        pygame.draw.rect(surface, color, pygame.Rect(pos, size))

    def draw_grid(self):
        rect_size = (20, 20)
        rect_color = (0, 0, 0)
        border_spacing_x, border_spacing_y = SCREEN.get_width() / 5, SCREEN.get_height() / 5

        rect_pos = (SCREEN.get_width() - SCREEN.get_rect().centerx, SCREEN.get_height() - SCREEN.get_rect().centery)
        self.draw_rect(SCREEN, rect_pos, rect_size, rect_color)


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
    pygame.display.flip()

pygame.quit()
