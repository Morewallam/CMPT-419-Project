'''
Class that controls enemy logic and drawing
'''
from dataclasses import dataclass, field
import math
import numpy as np
import pygame
from spritesheet import Spritesheet
from constants import Direction
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):

    def __init__(self, spritesheets, waypoints, type, deathhandler, end_handler, speed=1, direction=Direction.down):
        self.type = type
        pygame.sprite.Sprite.__init__(self)
        ss = Spritesheet(spritesheets[self.type])
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.direction = direction
        self.sprites = ss.load_many_strips((0, 0, 32, 32), 4, 4, -1)
        self.frame = 0
        self.image = self.sprites[self.direction.value][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.speed = speed
        self.death_handler = deathhandler
        self.end_handler = end_handler

    # Logic for what the enemy should do each update.
    def update(self):

        self.move()
        self.rotate()

        self.frame += 0.2

        if self.frame >= len(self.sprites[self.direction.value]):
            self.frame = 0

        self.image = self.sprites[self.direction.value][int(
            self.frame)]
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0], self.pos[1]-32)

    # The enemies move along a path that is loaded in.

    def move(self):
        # define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Perfrom logic for ending the game lol
            self.end_handler()
            self.kill()
            # calculate distance to target
        dist = self.movement.length()
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    # Change the sprite to match the direction the sprite is going
    def rotate(self):
        dist = self.target - self.pos
        # use distance to caluculate angel
        angle = math.atan2(-dist[1], dist[0])
        if angle >= -math.pi/4 and angle <= math.pi/4:
            self.direction = Direction.right
        elif angle > math.pi/4 and angle < 3*math.pi/4:
            self.direction = Direction.up
        elif angle > 3 * math.pi/4 or angle <= -3*math.pi/4:
            self.direction = Direction.left
        else:
            self.direction = Direction.down

    # the type of enemy
    def get_type(self):
        return self.type

    # Destrony a enemy
    def kill(self):
        self.death_handler()
        super().kill()
