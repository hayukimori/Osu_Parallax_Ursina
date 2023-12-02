from ursina import *

app = Ursina()


camera.overlay.color = color.black

logo = Sprite(name='ursina_splash', 
    parent=camera.ui, 
    texture='osu-resources/osu.Game.Resources/Textures/Intro/Welcome/welcome_text.png', 
    world_z=camera.overlay.z-1, 
    scale=.05,
    color=color.clear
)

logo.animate_color(
    color.white, 
    duration=2, 
    delay=1, 
    curve=curve.out_quint_boomerang
)

camera.overlay.animate_color(
    color.clear, 
    duration=1, 
    delay=2
)

destroy(logo, delay=5)

def splash_input(key):
    destroy(logo)

    camera.overlay.animate_color(
        color.clear, 
        duration=.25
    )

logo.input = splash_input


