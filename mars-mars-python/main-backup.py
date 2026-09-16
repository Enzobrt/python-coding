# TODO: Poner comentarios
# TODO: Poner warning de mucho velocidad

import pygame
import numpy as np
import math
# import keyboard

pygame.init()

SCREEN_SIZE = (800, 600)

MONITOR = pygame.display.Info()

WIDTH = MONITOR.current_w
HEIGHT = MONITOR.current_h
SCREEN_SIZE = (WIDTH, HEIGHT)

print(f"Size: {SCREEN_SIZE}")
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
# Sirve para cambiarle el nombre a la ventana
pygame.display.set_caption('Mars Mars')

screen_middle_x = SCREEN.get_rect().centerx
screen_middle_y = SCREEN.get_rect().centery

# Font
font = pygame.font.SysFont("JetBrains Mono", 15)
text_color = (255, 255, 255)  # White

# Background
background = (40, 40, 40)  # Dark gray

gradient_ground_color1 = (137, 3, 1)
gradient_ground_color2 = (142, 33, 3)

gradient_sky_color1 = (171, 227, 152)
gradient_sky_color2 = (93, 143, 79)

# Grounds
ground_color = (255, 255, 255)

ground1_size = [150, 20]
ground1_pos = [screen_middle_x - ground1_size[0]//2, 500]
ground1 = pygame.Rect(ground1_pos, ground1_size)

# kill obstacles
kill_bottom_color = (255, 0, 0)

kill_bottom_size = [SCREEN.get_rect().x, 10]
kill_bottom_pos = [0, ground1_pos[1] + 200]
kill_bottom = pygame.Rect(kill_bottom_pos, kill_bottom_size)

# Player variables
spawn_point = [ground1.centerx, ground1.top - 10]

player_pos = [ground1.centerx, ground1.top - 10]
player_size = [20, 20]
player_color = (0, 0, 255)  # Blue

player_jump = -12

gravity = 0.5
max_gravity = 20

# Camera
scroll = [0, 0]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a simple blue rectangle as the player
        self.image = pygame.Surface(player_size)
        self.image.fill(player_color)
        self.rect = self.image.get_rect()
        self.rect.center = player_pos

        self.alive = True

        self.player_fuel = 100
        self.player_using_jetpack = False
        self.player_jetpack_force = -8

        self.direction = "right"

        self.player_movement = 5

        self.jetpack_force_increase = 0
        self.gravity_force_increase = 0

        self.max_jetpack_force_increase = 2
        self.max_gravity_force_increase = -0.4

        # Physics variables
        self.vel_y = 0
        self.on_ground = True

    def current_fuel(self):
        return self.player_fuel

    def current_direction(self):
        return self.direction

    def respawn(self, spawn_point):
        player.rect.x = spawn_point[0]
        player.rect.y = spawn_point[1]
        # print("respawn")

    def ground_collision(self, grounds):
        self.on_ground = False
        hit = pygame.sprite.spritecollideany(player, grounds)
        if hit and player.vel_y >= 0:
            return True

    def check_kill_player(self, kill_obstacles, spawn_point):
        for kill_obstacle in kill_obstacles:
            if self.rect.bottom >= kill_obstacle.rect.top:
                player.respawn(spawn_point)

    def update(self, keys, spawn_point, grounds):
        if self.on_ground:
            self.player_movement = 8
            self.vel_y = 0

            self.jetpack_force_increase = 0
            self.gravity_force_increase = 0

            self.player_jetpack_force = -8
            self.max_jetpack_force_increase = 2
            self.max_gravity_force_increase = -0.4

        if self.player_using_jetpack or not self.on_ground:
            self.player_movement = 3

        # Stop player when hitting ground
        hit = pygame.sprite.spritecollideany(player, grounds)
        if player.ground_collision(ground_sprites):
            player.rect.bottom = hit.rect.top
            player.vel_y = 0
            player.on_ground = True

        # Movement
        if keys[pygame.K_a]:
            self.rect.x -= self.player_movement
            self.direction = "left"
        if keys[pygame.K_d]:
            self.rect.x += self.player_movement
            self.direction = "right"

        # Jumping logic
        """
        if keys[pygame.K_UP] | keys[pygame.K_w] and self.on_ground:
            self.vel_y = player_jump
            self.on_ground = False
        """

        if self.jetpack_force_increase >= self.max_jetpack_force_increase:
            self.jetpack_force_increase = self.max_jetpack_force_increase

        if self.gravity_force_increase <= self.max_gravity_force_increase:
            self.gravity_force_increase = self.max_gravity_force_increase

        # Jetpack logic
        if keys[pygame.K_SPACE] and self.player_fuel > 0:
            self.jetpack_force_increase += 0.1
            self.vel_y = self.player_jetpack_force
            self.vel_y -= self.jetpack_force_increase
            self.player_fuel -= 1
            self.player_using_jetpack = True
        else:
            self.player_using_jetpack = False
            self.jetpack_force_increase = 0

        if self.on_ground and not self.player_using_jetpack:
            self.player_fuel = 100000000

        if 0 <= self.player_fuel <= 10:
            self.player_jetpack_force = -11
            self.max_jetpack_force_increase = 3

        # Apply gravity
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # print(self.vel_y)

        if not self.on_ground:
            self.gravity_force_increase -= 0.4
            self.vel_y += 0.7
            self.vel_y += self.gravity_force_increase
            self.gravity_force_increase -= 0.5

        if self.vel_y >= max_gravity:
            self.vel_y = max_gravity

        if self.vel_y <= 0:
            self.vel_y = 0

        if self.vel_y == max_gravity and self.player_fuel <= 0 and player.ground_collision(grounds):
            self.on_ground = False
            self.vel_y = 0
            player.respawn(spawn_point)


class Ground(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface(rect.size)
        self.image.fill(ground_color)
        self.rect = rect


class KillObstacle(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface(rect.size)
        self.image.fill(kill_bottom_color)
        self.rect = rect


def draw_gradient_rect(surface, rect, color1, color2):
    # Create a 2x1 surface with the two colors
    temp_surf = pygame.Surface((1, 2), flags=pygame.SRCALPHA)
    temp_surf.fill(color1, (0, 0, 1, 1))
    temp_surf.fill(color2, (1, 0, 1, 1))

    # Scale it to the target rectangle
    scaled_surf = pygame.transform.smoothscale(temp_surf, (rect.width, rect.height))
    surface.blit(scaled_surf, rect)


def draw_mountains(surface, scroll_x, ground_y, color, base_h):
    spacing = 200
    start = int(scroll_x // spacing) * spacing
    for wx in range(start - spacing, start + SCREEN_SIZE[0] + spacing * 2, spacing):
        x = wx - scroll_x
        h = base_h * (0.5 + 0.5 * abs(math.sin(wx * 0.02)))
        pygame.draw.polygon(
            surface, color,
            [(x, ground_y), (x + spacing // 2, ground_y - h), (x + spacing, ground_y)])


player = Player()

ground1 = Ground(ground1)
ground_sprites = pygame.sprite.Group([ground1])

kill_bottom = KillObstacle(kill_bottom)
kill_obstacles = pygame.sprite.Group([kill_bottom])

player_sprite = pygame.sprite.Group(player)

all_sprites = pygame.sprite.Group(ground_sprites, kill_obstacles, player_sprite)

# Set up the clock
clock = pygame.time.Clock()
FPS = 60

# Set the game loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    # Player functions
    scroll[0] = player.rect.centerx - screen_middle_x
    scroll[1] = player.rect.centery - screen_middle_y

    player.update(keys, spawn_point, ground_sprites)
    player.check_kill_player(kill_obstacles, spawn_point)

    # Clamp to edge
    """
    clamp_rect = pygame.Rect(
        0, -10000, SCREEN.get_width(), SCREEN.get_height() + 10000)
    player.rect.clamp_ip(clamp_rect)
    """

    # Background color
    SCREEN.fill(gradient_sky_color1)

    # Sky gradient
    draw_gradient_rect(SCREEN, pygame.Rect(screen_middle_x - SCREEN.get_width() // 2, 100 - scroll[1], SCREEN.get_width(), SCREEN.get_height()), gradient_sky_color1, gradient_sky_color2)

    # Draw mountains
    draw_mountains(SCREEN, scroll[0], 500 - scroll[1], (70, 115, 60), 200)
    draw_mountains(SCREEN, scroll[0], 500 - scroll[1], (93, 143, 79), 130)

    # Ground gradient
    draw_gradient_rect(SCREEN, pygame.Rect(screen_middle_x - SCREEN.get_width() // 2, ground1_pos[1] - scroll[1], SCREEN.get_width(), SCREEN.get_height()), gradient_ground_color1, gradient_ground_color2)

    # Draw text
    facing_text = font.render(str(player.current_direction()), True, text_color)
    facing_text_pos = (20, 10)
    SCREEN.blit(facing_text, facing_text_pos)

    fuel_text = font.render(str(player.current_fuel()), True, text_color)
    fuel_text_pos = (20, 40)
    SCREEN.blit(fuel_text, fuel_text_pos)

    # Draw sprites
    for sprite in all_sprites:
        SCREEN.blit(sprite.image, (sprite.rect.x - scroll[0], sprite.rect.y - scroll[1]))

    pygame.display.flip()

pygame.quit()
