import pygame

from options import DISPLAY
from options import DELTATIME
from options import FPS
from options import clock
from options import font

from objects import ball
from points import score_l
from points import score_r
from objects import padel_l
# from objects import padel_r
from objects import padel_ai

pygame.init()

background_color = (30, 30, 30)

round = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f:
                round += 1
                print("round")
            if event.key == pygame.K_r:
                ball.start_new_round(DELTATIME, round)

    # Round
    if round <= 0:
        ball.start_new_round(DELTATIME, round)
        round += 1

    keys = pygame.key.get_pressed()

    DISPLAY.fill(background_color)

    # Update objects
    padel_l.update(
        keys[pygame.K_w], keys[pygame.K_s], DISPLAY, DELTATIME)
    # padel_r.update(keys[pygame.K_UP], keys[pygame.K_DOWN], DISPLAY, DELTATIME)

    padel_ai.update(DISPLAY, DELTATIME, ball.position)

    # Ball
    ball.update(DISPLAY, DELTATIME, round)

    ball.bounce_padel(padel_l)
    # ball.bounce_padel(padel_r)
    ball.bounce_padel(padel_ai)

    # Scores
    score_l.update(DISPLAY, font, ball.point_l)
    score_r.update(DISPLAY, font, ball.point_r)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
