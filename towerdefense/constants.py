import enum


SPRITES = {
    "black_dragon": 'BlackDragon.png',
    "red_dragon": 'RedDragon.png',
    "blue_dragon": 'BlueDragon.png',
    'yellow_dragon': 'YellowDragon.png',
    'ui_elements': 'UiIcons.png',
    'tileset': 'punyworld-overworld-tileset.png',
    'grass_tileset': 'Grass.png',
    'map': 'Map.png'
}

SOUNDS = {
    'select': 'Select 1.wav',
    'cancel': 'Cancel 1.wav',
    'jump': 'Jump 1.wav',
    'hit': 'Hit damage 1.wav',
    'confirm': 'Confirm 1.wav',
    'end': 'Blow 1.wav'
}


DESIRED_FPS = 60

WIDTH = 640
HEIGHT = 640
SIDE_PANEL = 200

MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT = 1, 2, 3


class Direction(enum.Enum):
    down = 0
    up = 1
    left = 2
    right = 3


class EnemyType(enum.Enum):
    happy = "happy"
    sad = "sad"
    angry = "angry"
    suprise = "suprise"
