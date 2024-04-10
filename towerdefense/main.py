import pygame
import constants as c
from game import TowerGame


# IMAGE_SPRITES = {}


# SCREENRECT = pygame.Rect(0, 0, c.WIDTH, c.HEIGHT)


def start_game():
    game = TowerGame.create((c.WIDTH + c.SIDE_PANEL, c.HEIGHT))
    game.start_game()


if __name__ == "__main__":
    start_game()
