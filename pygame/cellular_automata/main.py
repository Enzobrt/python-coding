import pygame

pygame.init()
DISPLAY_NATIVE_SIZE = (100, 100)
MONITOR_INFO = pygame.display.Info()
MONITOR_SIZE = (MONITOR_INFO.current_w, MONITOR_INFO.current_h)

DISPLAY_NATIVE = pygame.Surface(DISPLAY_NATIVE_SIZE)
MONITOR = pygame.display.set_mode(MONITOR_SIZE, pygame.NOFRAME)

FPS = 60
clock = pygame.time.Clock()

background_color = (30, 30, 30)
DISPLAY_NATIVE.fill(background_color)

# alive_color = (0, 180, 235)
alive_color = (255, 255, 255)
dead_color = background_color

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    left, middle, right = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if left:
        # print(f"Clicked at: {mouse_x}, {mouse_y}")
        # DISPLAY_NATIVE.set_at((mouse_x, mouse_y), alive_color)

        native_x = int(mouse_x * DISPLAY_NATIVE_SIZE[0] / MONITOR_SIZE[0])
        native_y = int(mouse_y * DISPLAY_NATIVE_SIZE[1] / MONITOR_SIZE[1])

        if 0 <= native_x < 100 and 0 <= native_y < 100:
            DISPLAY_NATIVE.set_at((native_x, native_y), alive_color)

    # Upscale screen
    scaled_surface = pygame.transform.scale(DISPLAY_NATIVE, MONITOR_SIZE)
    MONITOR.blit(scaled_surface, (0, 0))
    pygame.display.flip()
pygame.quit()
