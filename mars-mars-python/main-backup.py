# TODO: Poner comentarios
# TODO: Poner warning de mucho velocidad

import pygame
import numpy as np
import math
import random
import json
import os

MAP_FILE = "save.json"

pygame.init()

MAXIMIZED = False

MONITOR = pygame.display.Info()

WIDTH = MONITOR.current_w
HEIGHT = MONITOR.current_h
SCREEN_SIZE = (WIDTH, HEIGHT)

SCREEN_SIZE_SMALL = (800, 600)

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

kill_bottom_size = [SCREEN.get_rect().width, 10]
kill_bottom_pos = [0, ground1_pos[1] + 200]
kill_bottom = pygame.Rect(kill_bottom_pos, kill_bottom_size)

# Player variables
spawn_point = [ground1.centerx, ground1.top - 10]

player_pos = [ground1.centerx, ground1.top - 10]
player_size = [20, 20]
player_color = (0, 0, 255)  # Blue

CHECKPOINT_OFFSET_X = 0
CHECKPOINT_OFFSET_Y = 2

gravity = 0.5
max_gravity = 20

# Camera
scroll = [0, 0]


def platforms_to_data(grounds):
    return [[s.rect.x, s.rect.y, s.rect.width, s.rect.height] for s in grounds]


def save_map(name):
    last_platform = None
    if player.previous_platform is not None:
        rect = player.previous_platform.rect
        last_platform = [rect.x, rect.y, rect.width, rect.height]

    data = {
        "platforms": platforms_to_data(ground_sprites),
        "last_platform": last_platform,
        "platforms_stepped": player.platforms_stepped,
        "visited_platforms": [list(pos) for pos in player.visited_platforms],
    }

    with open(name, "w") as file:
        json.dump(data, file, indent=2)


def load_map(name):
    with open(name, "r") as file:
        data = json.load(file)

    old_grounds = ground_sprites.sprites()
    ground_sprites.empty()
    all_sprites.remove(old_grounds)

    for x, y, w, h in data["platforms"]:
        ground = Ground(pygame.Rect(x, y, w, h))
        ground_sprites.add(ground)
        all_sprites.add(ground)

    player.platforms_stepped = data["platforms_stepped"]
    player.visited_platforms = {tuple(pos) for pos in data.get("visited_platforms", [])}

    player.previous_platform = None
    if data["last_platform"] is not None:
        lx, ly, lw, lh = data["last_platform"]
        for ground in ground_sprites:
            if ground.rect.x == lx and ground.rect.y == ly:
                player.previous_platform = ground
                break

    return data


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
        self.current_platform_pos = None
        self.previous_platform = None
        self.platforms_stepped = 0
        self.visited_platforms = set()

    def current_fuel(self):
        return self.player_fuel

    def current_direction(self):
        return self.direction

    def current_platform(self, grounds):
        hit = pygame.sprite.spritecollideany(player, grounds)
        self.platform_object = hit if hit and player.vel_y >= 0 else None
        self.current_platform_pos = self.platform_object.rect.topleft if self.platform_object else None
        return self.platform_object

    def is_new_platform(self, current, was_on_ground):
        if current is None or was_on_ground:
            return False
        if current.rect.topleft in self.visited_platforms:
            return False
        self.visited_platforms.add(current.rect.topleft)
        self.platforms_stepped += 1
        return True

    def checkpoint_pos(self):
        if self.previous_platform is not None:
            rect = self.previous_platform.rect
            pos = [rect.x + CHECKPOINT_OFFSET_X,
                   rect.top - self.rect.height - CHECKPOINT_OFFSET_Y]
            if pos[1] + self.rect.height < kill_bottom.rect.top:
                return pos
        return list(spawn_point)

    def respawn(self):
        self.rect.x, self.rect.y = self.checkpoint_pos()
        self.vel_y = 0
        self.on_ground = False
        self.player_using_jetpack = False
        # print("respawn")

    def ground_collision(self, grounds):
        self.on_ground = False
        hit = pygame.sprite.spritecollideany(player, grounds)
        if hit and player.vel_y >= 0:
            return True

    def check_kill_player(self, kill_obstacles):
        for kill_obstacle in kill_obstacles:
            if self.rect.bottom >= kill_obstacle.rect.top:
                self.respawn()

    def update(self, keys, grounds):
        if self.on_ground:
            self.player_movement = 8
            self.vel_y = 0

            self.jetpack_force_increase = 0
            self.gravity_force_increase = 0

            self.player_jetpack_force = -8
            self.max_jetpack_force_increase = 2
            self.max_gravity_force_increase = -0.4

        if self.player_using_jetpack or not self.on_ground:
            self.player_movement = 4.5

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
            self.player_fuel = 100

        if 0 <= self.player_fuel <= 10:
            self.player_jetpack_force = -11
            self.max_jetpack_force_increase = 3

        # Apply gravity
        self.vel_y += gravity
        self.rect.y += self.vel_y

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
            self.respawn()


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


def generate_platforms(current_platform, color, size):
    if SCREEN.get_height() <= 800:
        platform_x_range = (250, SCREEN.get_height() - 200)
    else:
        platform_x_range = (300, SCREEN.get_height() // 2)

    if player.rect.y >= 350:
        platform_y_range = (0, 150)
    elif player.rect.y <= -100:
        platform_y_range = (-150, 0)
    else:
        platform_y_range = (-150, 100)
    spacing = (random.randint(platform_x_range[0], platform_x_range[1]), random.randint(platform_y_range[0], platform_y_range[1]))
    platform = pygame.Rect((current_platform.rect.x + spacing[0], current_platform.rect.y - spacing[1]), size)
    ground = Ground(platform)
    ground_sprites.add(ground)
    all_sprites.add(ground)


def start_new_game():
    old_grounds = ground_sprites.sprites()
    ground_sprites.empty()
    all_sprites.remove(old_grounds)

    first_ground = Ground(pygame.Rect(ground1_pos, ground1_size))
    ground_sprites.add(first_ground)
    all_sprites.add(first_ground)

    player.previous_platform = first_ground
    player.platforms_stepped = 1
    player.visited_platforms = {first_ground.rect.topleft}
    player.player_fuel = 100
    player.respawn()

    generate_platforms(first_ground, ground_color, ground1_size)
    return first_ground


player = Player()

ground1 = Ground(ground1)
ground_sprites = pygame.sprite.Group([ground1])

kill_bottom = KillObstacle(kill_bottom)
kill_obstacles = pygame.sprite.Group([kill_bottom])

player_sprite = pygame.sprite.Group(player)

all_sprites = pygame.sprite.Group(ground_sprites, kill_obstacles, player_sprite)

if os.path.exists(MAP_FILE):
    load_map(MAP_FILE)
else:
    start_new_game()

player.respawn()

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

            elif event.key == pygame.K_f:
                MAXIMIZED = not MAXIMIZED
                pygame.display.set_mode(SCREEN_SIZE if MAXIMIZED else SCREEN_SIZE_SMALL, pygame.RESIZABLE)
                screen_middle_x = SCREEN.get_rect().centerx
                screen_middle_y = SCREEN.get_rect().centery

            elif event.key == pygame.K_p:
                if os.path.exists(MAP_FILE):
                    os.remove(MAP_FILE)
                start_new_game()

        elif event.type == pygame.VIDEORESIZE:
            # Recreate surface with new dimensions
            SCREEN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    keys = pygame.key.get_pressed()

    # Player functions
    scroll[0] = player.rect.centerx - screen_middle_x + 300
    scroll[1] = player.rect.centery - screen_middle_y

    was_on_ground = player.on_ground
    player.update(keys, ground_sprites)
    player.check_kill_player(kill_obstacles)

    kill_bottom.rect.centerx = player.rect.centerx + 300 + 300


    current = player.current_platform(ground_sprites)
    if player.is_new_platform(current, was_on_ground):
        print("Nueva plataforma:", current.rect.topleft)
        generate_platforms(current, ground_color, ground1_size)
    if current is not None:
        player.previous_platform = current

    # Background color
    SCREEN.fill(gradient_sky_color1)

    # Sky gradient
    draw_gradient_rect(SCREEN, pygame.Rect(screen_middle_x - SCREEN.get_width() // 2, 100 - scroll[1], SCREEN.get_width(), SCREEN.get_height()), gradient_sky_color1, gradient_sky_color2)

    # Draw mountains
    draw_mountains(SCREEN, scroll[0], 500 - scroll[1], (70, 115, 60), 200)
    draw_mountains(SCREEN, scroll[0], 500 - scroll[1], (93, 143, 79), 130)

    # Ground gradient
    draw_gradient_rect(SCREEN, pygame.Rect(screen_middle_x - SCREEN.get_width() // 2, ground1_pos[1] - scroll[1], SCREEN.get_width(), SCREEN.get_height()), gradient_ground_color1, gradient_ground_color2)

    # Player position text
    player_pos = (player.rect.x, player.rect.y)
    player_position_text = font.render(str(player_pos), True, text_color)
    player_position_text_pos = (20, 70)
    SCREEN.blit(player_position_text, player_position_text_pos)

    # Draw text
    facing_text = font.render(str(player.current_direction()), True, text_color)
    facing_text_pos = (20, 10)
    SCREEN.blit(facing_text, facing_text_pos)

    fuel_text = font.render(str(player.current_fuel()), True, text_color)
    fuel_text_pos = (20, 40)
    SCREEN.blit(fuel_text, fuel_text_pos)

    platforms_text = font.render(str(player.platforms_stepped), True, text_color)
    platforms_text_pos = (20, 100)
    SCREEN.blit(platforms_text, platforms_text_pos)

    # Draw sprites
    for sprite in all_sprites:
        SCREEN.blit(sprite.image, (sprite.rect.x - scroll[0], sprite.rect.y - scroll[1]))

    pygame.display.flip()


save_map(MAP_FILE)

pygame.quit()
