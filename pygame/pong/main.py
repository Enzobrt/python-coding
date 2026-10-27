import pygame
import random
import numpy as np

import objects
import options

pygame.init()

background_color = (30, 30, 30)


def start_new_round(delta, ball, round):
    ball.position = [options.DISPLAY.get_rect(
    ).centerx, options.DISPLAY.get_rect().centery]

    initial_speed = 100

    ball_angle = random.uniform(0, 2 * np.pi)

    ball_vx = np.cos(ball_angle) * initial_speed
    ball_vy = np.sin(ball_angle) * initial_speed
    ball_v = [ball_vx, ball_vy]
    print(ball_v)
    ball.speed_vector = ball_v


def bounce_ball(ball, screen, padel_position):
    pass


round = 0

running = True
while running:
    if not np:
        assert ("Numpy isnt installed")

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
                start_new_round(options.DELTATIME, objects.ball, round)

    if round <= 0:
        start_new_round(options.DELTATIME, objects.ball, round)
        round += 1

    keys = pygame.key.get_pressed()

    options.DISPLAY.fill(background_color)
    objects.padel_l.update(
        keys[pygame.K_w], keys[pygame.K_s], options.DISPLAY, options.DELTATIME)
    objects.padel_r.update(
        keys[pygame.K_UP], keys[pygame.K_DOWN], options.DISPLAY, options.DELTATIME)
    objects.ball.update(options.DISPLAY, options.DELTATIME)

    pygame.display.flip()
    options.clock.tick(options.FPS)

pygame.quit()
