from ursina import *


class PlayerCam(Entity):
    def __init__(self, target, smoothness=1):
        super().__init__()

        self.target = target
        self.smoothness = smoothness
        self.sensitivity = 50

        mouse.locked = True
        camera.fov = 120

        camera.position = self.target.world_position + Vec3(0, self.target.eye_height, 0)

    def update(self):
        # Poner la camara en la posicion del jugador
        camera.position = self.target.world_position + Vec3(0, self.target.eye_height, 0)

        # Girar la camara con la posicion del raton
        camera.rotation_y += mouse.velocity.x * self.sensitivity
        camera.rotation_x -= mouse.velocity.y * self.sensitivity

        # Limitar rotacion camara (para evitar dar la vuelta)
        camera.rotation_x = clamp(camera.rotation_x, -90, 80)
