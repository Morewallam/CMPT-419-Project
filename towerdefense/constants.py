import enum


SPRITES = {
    "black_dragon": 'BlackDragon.png',
    "red_dragon": 'RedDragon.png',
    "blue_dragon": 'BlueDragon.png',
    'yellow_dragon': 'YellowDragon.png',
    'ui_elements': 'UiIcons.png',
    'tileset': 'punyworld-overworld-tileset.png',
    'grass_tileset': 'Grass.png'
}


DESIRED_FPS = 60

WIDTH = 600
HEIGHT = 600

MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT = 1, 2, 3


class Direction(enum.Enum):
    down = 0
    up = 1
    left = 2
    right = 3
