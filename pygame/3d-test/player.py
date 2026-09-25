from ursina import *


class player(Entity):
    def __init__(self, limits):
        super().__init__()

        self.movement = 6
        self.jump_force = 0.3
        self.gravity = 0.01
        self.on_ground = False

        self.vel_y = 0

        # Map limits, shared with the ground and the camera
        self.limits = limits
        self.half_width = 0.5

        self.player_entity = Entity(
            parent = self,
            model = "cube",

            color = color.orange,

            scale_x = 1,
            scale_y = 2,
            scale_z = 1,

            collider = "box"
            )

        self.position = (0, 4, 0)

    def keep_inside_limits(self):
        # Push the player back inside the map on each axis separately,
        # leaving half a body of margin so it never hangs over the edge
        max_x = self.limits.half_x - self.half_width
        max_z = self.limits.half_z - self.half_width

        self.player_entity.x = clamp(self.player_entity.x, -max_x, max_x)
        self.player_entity.z = clamp(self.player_entity.z, -max_z, max_z)

    def player_collision(self):
        # Floor detection
        hit_floor = raycast(
            self.player_entity.world_position + Vec3(0, -1, 0),
            self.player_entity.down,
            distance = 0.1 + self.vel_y,
            ignore = [self, self.player_entity]
            )

        self.on_ground = bool(hit_floor)

    def input(self, key):
        if key ==  "space":
            if self.on_ground:
                self.on_ground = False
                self.vel_y -= self.jump_force

    def update(self):
        # Basic player movement
        if held_keys["d"]:
            self.player_entity.x += self.movement * time.dt

        if held_keys["a"]:
            self.player_entity.x -= self.movement * time.dt

        if held_keys["w"]:
            self.player_entity.z += self.movement * time.dt

        if held_keys["s"]:
            self.player_entity.z -= self.movement * time.dt

        # Block the player from leaving the map
        self.keep_inside_limits()

        # Detect collisions
        self.player_collision()

        # Apply gravity
        if self.on_ground:
            self.vel_y = 0
        else:
            self.vel_y += self.gravity
            self.player_entity.y -= self.vel_y
