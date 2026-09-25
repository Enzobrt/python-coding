from level import ground
from player import player
from cam import player_cam
from ursina import *

app = Ursina()

ground = ground()
player = player(ground)
player_cam = player_cam(player.player_entity, ground)

app.run()
