from panda3d.core import MaterialAttrib, TextureAttrib

from ursina import Entity, Texture, color


def _piezas(modelo):
    for hijo in modelo.getChildren():
        if hijo.findAllMatches('**/+GeomNode').isEmpty():
            yield from _piezas(hijo)
        else:
            yield hijo


def _aplicar_material(entidad):
    geoms = entidad.model.findAllMatches('**/+GeomNode')
    if len(geoms) == 0:
        return

    node = geoms[0].node()
    if node.get_num_geoms() == 0:
        return

    state = node.get_geom_state(0)
    if not state:
        return

    attrib_texturas = state.get_attrib(TextureAttrib)
    if attrib_texturas:
        for stage in attrib_texturas.get_on_stages():
            if stage.get_name() == 'Base Color':
                entidad.texture = Texture(stage.get_texture())
                break

    attrib_material = state.get_attrib(MaterialAttrib)
    if attrib_material:
        material = attrib_material.get_material()
        if material:
            entidad.color = color.rgba(*material.get_base_color())


def cargar_escena(ruta, position=(0, 0, 0)):
    escena = Entity(model=ruta, position=position)

    for pieza in _piezas(escena.model):
        entidad = Entity(
            parent=escena,
            name=pieza.getName(),
            position=pieza.getPos(escena),
            scale=pieza.getScale(escena),
            quaternion=pieza.getQuat(escena),
        )
        pieza.wrtReparentTo(entidad)
        entidad.model = pieza
        entidad.collider = 'box'
        _aplicar_material(entidad)

    return escena
