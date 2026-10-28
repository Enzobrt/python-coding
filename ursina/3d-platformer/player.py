from ursina import *


class Player(Entity):
    def __init__(self):
        super().__init__()

        self.player_entity = Entity(
            parent=self,
            model="cube",
            collider="box",

            color=color.blue,
            texture="white_cube",

            position=(0, 1, 0),
            scale=(1, 2, 1)
        )
        self.position = (0, 6, 0)

        self.movement = 6
        self.jump_force = 0.3
        self.coyote_time = 0.3
        self.on_ground = False

        self.gravity = 0.01
        self.max_y_speed = 1

        self.height = self.player_entity.y + self.player_entity.scale_y / 2
        self.eye_height = self.height - 0.3

        self.vel_y = 0
        self.ground_distance = 9999

    def player_collision(self):
        # El rayo nace en la cabeza para ver la cara superior de los escalones
        raycast_floor = raycast(
            self.world_position + Vec3(0, self.height, 0),
            self.down,
            ignore=[self, self.player_entity]
        )

        # Solo cuenta como suelo una superficie horizontal, y como maximo medio cuerpo por encima
        # (asi se pueden subir escalones; el snap es seguro porque la normal esta validada)
        if raycast_floor and raycast_floor.world_normal.y > 0.7:
            altura = raycast_floor.world_point.y - self.world_position.y

            if altura > 0.5:
                # el suelo esta mucho mas arriba: es un techo, no suelo
                self.ground_distance = 9999
            elif altura > 0:
                # el suelo esta mas arriba: es un escalon y se sube
                self.y = raycast_floor.world_point.y
                self.ground_distance = 0
            elif altura > -0.1:
                # esta apoyado: se pega al suelo. Sin esto, bajando una cuesta el suelo
                # se aleja en cada frame, el jugador queda flotando a medio camino,
                # nunca llega a contar como apoyado y no puede saltar
                self.y = raycast_floor.world_point.y + 0.02
                self.ground_distance = 0.02
            else:
                self.ground_distance = -altura
        else:
            self.ground_distance = 9999

        self.on_ground = self.ground_distance < 0.05

    def wall_ahead(self, direction):
        feet_ray = raycast(
            self.world_position + Vec3(0, 0.5, 0),
            direction,
            distance=0.5,
            ignore=[self, self.player_entity]
        )
        head_ray = raycast(
            self.world_position + Vec3(0, self.height - 0.1, 0),
            direction,
            distance=0.5,
            ignore=[self, self.player_entity]
        )
        return feet_ray or head_ray

    def update(self):
        self.player_collision()

        self.eye_height = self.player_entity.y + self.player_entity.scale_y / 2 - 0.3

        # Mover al jugador relativo a la camara
        forward = camera.forward
        forward.y = 0
        forward = forward.normalized()

        right = camera.right
        right.y = 0
        right = right.normalized()

        x = held_keys["d"] - held_keys["a"]
        z = held_keys["w"] - held_keys["s"]

        if x or z:
            direction = (right * x + forward * z).normalized()

            if not self.wall_ahead(direction):
                self.position += direction * 5 * time.dt

            else:
                # Hay pared delante: moverse solo por los ejes libres para deslizarse
                # en vez de quedarse pegado a la pared
                if x and not self.wall_ahead(right * x):
                    self.position += right * x * 5 * time.dt

                if z and not self.wall_ahead(forward * z):
                    self.position += forward * z * 5 * time.dt

        # Saltar
        if held_keys["space"] and self.on_ground and self.coyote_time > 0:
            self.on_ground = False
            self.vel_y = -self.jump_force

        # Aplicar gravedad
        if self.on_ground:
            self.vel_y = 0
            self.coyote_time = 0.3
        else:
            self.vel_y += self.gravity * time.dt * 60
            self.coyote_time -= time.dt

            if self.vel_y >= self.max_y_speed:
                self.vel_y = self.max_y_speed

            # No se puede caer mas de lo que hay hasta el suelo
            self.y -= min(self.vel_y * time.dt * 60,
                          self.ground_distance - 0.02)
