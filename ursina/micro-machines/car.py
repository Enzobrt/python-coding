from ursina import Entity
from ursina import color
from ursina import held_keys
from ursina import time
from ursina import load_model
from ursina import load_texture

from functions import lerp

car_model = load_model("car")
car_texture = load_texture("car_texture")


class Player(Entity):
    def __init__(self):
        super().__init__()

        self.player_entity = Entity(
            parent=self,
            model=car_model,
            texture=car_texture,
            collider="box",

            # color = color.blue,

            position=(0, 1, 0),
            scale=(1, 1, 1)
        )
        # self.origin_z = 0.5

        self.speed = 0
        self.max_forward_speed = 10
        self.max_reverse_speed = -10

        self.acceleration = 0.1
        self.friction = 3.5

        self.drifting = False
        self.grip = -0.1

        self.turning = 0
        self.turning_speed = 12
        self.max_turning = 150

    def update(self):
        x = held_keys["d"] - held_keys["a"]
        z = held_keys["w"] - held_keys["s"]

        # Mover al jugador relativo a la camara
        forward = self.forward
        forward.y = 0
        forward = forward.normalized()

        right = self.right
        right.y = 0
        right = right.normalized()

        x = held_keys["d"] - held_keys["a"]
        z = held_keys["w"] - held_keys["s"]

        if held_keys["space"]:
            self.drifting = True

            self.max_turning = 300
            self.turning_speed = 20
            self.max_forward_speed = 7
        else:
            self.drifting = False

            self.max_turning = 150
            self.turning_speed = 12
            self.max_forward_speed = 10

        if self.speed <= self.max_reverse_speed:
            self.speed = self.max_reverse_speed

        target_steering = x * self.max_turning

        self.turning = lerp(
            self.turning,
            target_steering,
            self.turning_speed * time.dt
        )

        if self.drifting:
            self.x += self.drifting * time.dt * x + self.grip
            self.z += self.drifting * time.dt * z - self.grip
        else:
            self.rotation_y += self.turning * time.dt * abs(z)

        if z and not self.drifting:
            self.speed += z * self.acceleration
            self.speed = min(self.speed, self.max_forward_speed)

        else:
            self.speed = lerp(
                self.speed,
                0,
                min(self.friction * time.dt, 1)
            )
        self.position += forward * self.speed * time.dt


player = Player()
