from ursina import camera
from ursina import Entity
# from ursina import Vec3

from car import player


class Camera(Entity):
    def __init__(self):
        super().__init__()

        self.sensitivity = 50
        camera.fov = 90
        camera.position = (0, 10, 0)
        camera.rotation = (0, 0, 0)

        self.offset = (0, 12, -6)

    def update(self):
        camera.look_at(player)
        camera.position = player.position + self.offset


cam = Camera()
