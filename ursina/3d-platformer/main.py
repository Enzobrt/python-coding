from ursina import *

from scenes_pbr import cargar_escena
# from scenes import cargar_escena
from player import Player
from cam import PlayerCam

app = Ursina()

Entity.default_shader = None

mouse.position = (0, 0, 0)

# Window options
window.title = "Test game"
window.borderless = False
window.vsync = True
window.fps_counter.enabled = True
window.exit_button.visible = False

player = Player()
player_cam = PlayerCam(player)

# Load scene
escena = cargar_escena('scenes/test.glb', position=(0, 0.5, 0))

app.run()
