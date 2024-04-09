from dataclasses import dataclass, field
import numpy as np
import pygame
from spritesheet import Spritesheet
from constants import Direction


class Enemy(pygame.sprite.Sprite):

    def __init__(self, spritesheet, pos, direction=Direction.down):
        pygame.sprite.Sprite.__init__(self)
        ss = Spritesheet(spritesheet)
        self.direction = direction
        self.loadingsprites = ss.load_many_strips((0, 0, 32, 32), 4, 4, -1)
        self.image = self.loadingsprites[self.direction.value][0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def move(self):
        self.rect.x += 1
