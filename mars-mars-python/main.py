import pygame

pygame.init()

SCREEN = pygame.display.Info()

WIDTH = SCREEN.current_w
HEIGHT = SCREEN.current_h
SCREEN_SIZE = (WIDTH, HEIGHT)

WIDTH_MIDDLE = WIDTH // 2
HEIGHT_MIDDLE = HEIGHT // 2

print(f"Size: {WIDTH}, {HEIGHT}")

# WINDOW = pygame.display.set_mode(SCREEN_SIZE)
WINDOW = pygame.display.set_mode(800, 600)

pygame.display.set_caption('Mars Mars')

# Font
font = pygame.font.SysFont("JetBrains Mono", 15)
text_color = (255, 255, 255)  # White

# Background
background_color = (171, 227, 152)

# Player
player_image = pygame.image.load("assets/player/player_land.png").convert_alpha()

running = True

clock = pygame.time.Clock()
FPS = 60

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Detect edge
    """
    clamp_rect = pygame.Rect(
        0, -10000, WINDOW.get_width(), WINDOW.get_height() + 10000)
    player.rect.clamp_ip(clamp_rect)
    """

    WINDOW.fill(background_color)

    # Draw player
    WINDOW.blit(player_image, (WIDTH_MIDDLE, HEIGHT_MIDDLE))

    pygame.display.flip()

pygame.quit()
