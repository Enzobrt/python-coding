from ursina import *

app = Ursina(
    # borderless=True,
    fullscreen=False,
    title="Micro machines",
    # icon="",
    vsync=True,
    # use_ingame_console=True,
    # show_ursina_splash=True
)
window.fps_counter.enabled = True

from level import floor
from cam import cam
from car import player


def input(key):
    if key == "escape":
        application.quit()


app.run()
