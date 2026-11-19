from ursina import Entity
from ursina import color


class Floor(Entity):
    def __init__(self, position):
        super().__init__()

        self.floor_entity = Entity(
            # parent=self,
            model="cube",
            collider="box",

            color=color.white,
            texture="white_cube",

            position=position,
            scale=(1, 0, 1)
        )


size = (10, 0, 10)

for x in range(size[0]):
    for z in range(size[2]):
        floor = Floor(position=(x, 0, z))
