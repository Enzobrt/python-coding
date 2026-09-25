from ursina import *


class ground(Entity):
    def __init__(self):
        super().__init__()

        self.ground_entity = Entity(
            parent = self,
            model = "cube",

            color = color.green,

            scale_x = 30,
            scale_y = 1,
            scale_z = 50,

            collider = "box"
            )

        self.position = (0, 0, 0)

        # Map limits, derived from the ground size so they can't get out of sync
        self.half_x = self.ground_entity.scale_x / 2
        self.half_z = self.ground_entity.scale_z / 2

        self.create_walls()

    def create_walls(self):
        self.walls = []

        wall_height = 20
        wall_thickness = 1

        for x in (-self.half_x - wall_thickness / 2, self.half_x + wall_thickness / 2):
            self.walls.append(Entity(
                parent = self,
                position = (x, wall_height / 2, 0),
                scale = (wall_thickness, wall_height, self.half_z * 2),
                collider = "box",
                visible = False
                ))

        for z in (-self.half_z - wall_thickness / 2, self.half_z + wall_thickness / 2):
            self.walls.append(Entity(
                parent = self,
                position = (0, wall_height / 2, z),
                scale = (self.half_x * 2, wall_height, wall_thickness),
                collider = "box",
                visible = False
                ))
