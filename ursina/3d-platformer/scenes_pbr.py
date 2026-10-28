from ursina import Entity, Vec2, Vec3, color
from ursina.lights import AmbientLight, DirectionalLight


def _piezas(modelo):
    for hijo in modelo.getChildren():
        if hijo.findAllMatches('**/+GeomNode').isEmpty():
            yield from _piezas(hijo)
        else:
            yield hijo


def _crear_luces():
    sol = DirectionalLight(shadow_map_resolution=Vec2(2048, 2048))
    sol.position = (20, 35, -15)
    sol.look_at(Vec3(0, 0, 0), axis=Vec3.back)
    sol.color = color.rgba(1.4, 1.4, 1.4, 1)

    lente = sol._light.get_lens()
    lente.set_near_far(1, 200)
    lente.set_film_offset(Vec2(0, 0))
    lente.set_film_size(70, 70)

    ambiente = AmbientLight()
    ambiente.color = color.rgba(0.35, 0.35, 0.42, 1)

    Entity(
        model='sphere',
        position=(-38, 131, -53),
        scale=14,
        color=color.rgb(1, 0.93, 0.75),
        unlit=True,
    )


def cargar_escena(ruta, position=(0, 0, 0)):
    escena = Entity(model=ruta, position=position, shader=None)

    for pieza in _piezas(escena.model):
        entidad = Entity(
            parent=escena,
            name=pieza.getName(),
            shader=None,
            position=pieza.getPos(escena),
            scale=pieza.getScale(escena),
            quaternion=pieza.getQuat(escena),
        )
        pieza.wrtReparentTo(entidad)
        entidad.model = pieza
        entidad.collider = 'box'

    _crear_luces()

    return escena
