from math import ceil, cos, radians, sin

from ursina import *


# El cubo de ursina son 6 cuadrados (2 triangulos cada uno). Acá van sus vertices y
# sus caras con los uv de toda la textura, igual que el cubo original, para que se vea
# lo mismo. Lo que cambia es que cada voxel arma la malla solo con las caras que hay
# que dibujar: las que tapan otros cubos o las que quedan bajo el piso no se dibujan
# y no le cuestan nada a la GPU.
VERTICES_CUBO = (
    Vec3(-.5, -.5, -.5), Vec3(.5, -.5, -.5), Vec3(.5, .5, -.5), Vec3(-.5, .5, -.5),
    Vec3(-.5, -.5, .5), Vec3(.5, -.5, .5), Vec3(.5, .5, .5), Vec3(-.5, .5, .5)
)

UV_CARA = ((0, 0), (1, 0), (1, 1), (0, 1))

CARAS_CUBO = {
    "arriba": (3, 2, 6, 7),      # +y, la cara que se pisa
    "abajo": (4, 5, 1, 0),       # -y, la que mira al piso
    "derecha": (1, 5, 6, 2),     # +x
    "izquierda": (4, 0, 3, 7),   # -x
    "frente": (0, 1, 2, 3),      # +z
    "atras": (5, 4, 7, 6)        # -z
}

TODAS_LAS_CARAS = tuple(CARAS_CUBO)


def malla_de_caras(caras):
    vertices = []
    triangulos = []
    uvs = []
    for cara in caras:
        cuaderno = CARAS_CUBO[cara]
        base = len(vertices)
        vertices.extend(VERTICES_CUBO[indice] for indice in cuaderno)
        triangulos.append(tuple(range(base, base + 4)))
        uvs.extend(UV_CARA)
    return Mesh(vertices=vertices, triangles=triangulos, uvs=uvs, mode="triangle")


class Voxel(Entity):
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), color=color.white, scale=(1, 1, 1), caras=TODAS_LAS_CARAS):
        super().__init__()
        self.ground_entity = Entity(
            parent=self,
            model=malla_de_caras(caras),

            position=position,
            scale=scale,
            rotation=rotation,

            color=color,
            texture="white_cube"
        )

        # la caja de colision va aparte y completa: por mas que falten caras para
        # dibujar, el cubo sigue chocando igual que antes
        self.ground_entity.collider = BoxCollider(self.ground_entity)
        self.ground_entity.double_sided = False


def generate_ground(x, y, z, scale, color):
    for scale_x in range(scale[0]):
        for scale_z in range(scale[2]):
            # de los seis cuadrados solo se ven el de arriba y los del borde:
            # los del medio quedan tapados por los cubos vecinos
            caras = ["arriba"]
            if scale_x == 0:
                caras.append("izquierda")
            if scale_x == scale[0] - 1:
                caras.append("derecha")
            if scale_z == 0:
                caras.append("frente")
            if scale_z == scale[2] - 1:
                caras.append("atras")

            voxel = Voxel(
                position=(
                    (x + scale_x,
                     y, z + scale_z)
                ),
                color=color,
                caras=caras
            )


def generate_ramp(position, scale, color, angle=10, direction=0):
    rotation = (0, direction, -angle)

    voxel = Voxel(position=position, rotation=rotation,
                  color=color, scale=scale)


def generate_ramp_voxel(position, scale, color, angle=10, direction=0):
    # position = punto donde arranca la superficie de la rampa (x, altura del suelo, z)
    # scale = (largo de la rampa en el suelo, 1, ancho de lado a lado)
    # angle = inclinacion en grados
    # direction = hacia donde sube: 0 -> +x, 90 -> -z, 180 -> -x, 270 -> +z
    angulo = radians(angle)
    giro = radians(direction)

    # hacia donde avanza la rampa y hacia donde se ensancha
    adelante = Vec3(cos(giro), 0, -sin(giro))
    lado = Vec3(sin(giro), 0, cos(giro))

    # dos caras superiores encajan justas si sus cubos van separados cos(angulo):
    # asi quedan en un solo plano, sin huecos ni solapes. Por debajo de ese plano
    # los cubos se meten uno dentro del otro, y de ahi sale el escalon que se ve
    paso = cos(angulo)
    rise = sin(angulo)

    # el centro de la cara de arriba de un cubo inclinado queda sin(angulo)/2 mas
    # adelante en la cuesta, y cos(angulo)/2 por encima del centro del cubo
    corrimiento = sin(angulo) / 2
    medio = cos(angulo) / 2

    largo_total = ceil(scale[0] / paso)

    for largo in range(largo_total):
        for ancho in range(scale[2]):
            # en el cubo local la cara de arriba es +y, la de cuesta abajo es -x
            # (que es +x derecho = adelante) y el ancho va de lado a lado en +z.
            # la cara de +x queda metida dentro del cubo siguiente, asi que no se
            # dibuja, y las caras de los costados solo en la primera y la ultima
            # fila, porque en el medio quedan pegadas una a otra
            caras = ["arriba", "abajo", "izquierda"]
            if ancho == 0:
                caras.append("frente")
            if ancho == scale[2] - 1:
                caras.append("atras")

            voxel = Voxel(
                position=(
                    Vec3(position)
                    + adelante * (paso * largo + corrimiento)
                    + lado * ancho
                    + Vec3(0, rise * largo - medio, 0)
                ),
                rotation=(0, direction, -angle),
                color=color,
                caras=caras
            )


# ground = generate_ground(0, 0, 0, (20, 1, 20), color.white)
# ceiling = generate_ground(0, 10, 0, (20, 0, 20), color.lime)

# ramp = generate_ramp((5, 5.1, -14.5), (30, 1, 5), color.red, angle=20, direction=90)

# ramp = generate_ramp_voxel((5, 0.5, 2), (10, 1, 5), color.red, angle=40, direction=0)
