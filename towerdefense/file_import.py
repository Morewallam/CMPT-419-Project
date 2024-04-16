'''
File that makes functions for importing assests
'''
import importlib.resources
import pygame


def load(module_path, name):
    return importlib.resources.path(module_path, name)


def import_image(asset_name: str):
    with load("towerdefense.assests.gfx", asset_name) as resourse:
        return pygame.image.load(resourse).convert_alpha()


def import_map(map_name: str):
    with load("towerdefense.assests.levels", map_name) as resourse:
        return resourse


def import_sound(asset_name: str):
    """
    Imports, as a sound effect, `asset_name`.
    """
    with load("towerdefense.assests.audio", asset_name) as resource:
        return pygame.mixer.Sound(resource)
