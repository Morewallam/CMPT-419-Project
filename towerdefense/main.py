import pygame
import constants as c
from game import TowerGame


def start_game():
    game = TowerGame.create((c.WIDTH + c.SIDE_PANEL, c.HEIGHT))
    game.start_game()


if __name__ == "__main__":
    start_game()
