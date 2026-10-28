import pygame

import options

from objects import ball
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
                ball.start_new_round(options.DELTATIME, round)

    # Round
    if round <= 0:
        ball.start_new_round(options.DELTATIME, round)
        round += 1

    keys = pygame.key.get_pressed()

    options.DISPLAY.fill(background_color)

    # Update objects
    padel_l.update(
        keys[pygame.K_w], keys[pygame.K_s], options.DISPLAY, options.DELTATIME)
    # padel_r.update(keys[pygame.K_UP], keys[pygame.K_DOWN], options.DISPLAY, options.DELTATIME)

    padel_ai.update(options.DISPLAY, options.DELTATIME, ball.position)

    # Ball
    ball.update(options.DISPLAY, options.DELTATIME, round)

    ball.bounce_padel(padel_l)
    # ball.bounce_padel(padel_r)
    ball.bounce_padel(padel_ai)

    pygame.display.flip()
    options.clock.tick(options.FPS)

pygame.quit()
