'''
Class for hankding all the world  data
including things like level, score, spawntimes, path and the background
'''

import math
import pygame

from spawner import EnemySpawner
from constants import EnemyType
import random

SPAWN_TIME_SCALER = 0.9
SPEED_SCALER = 1.001
SCORE_PER_LEVEL = 15


class World():
    def __init__(self, data, map_image):
        self.image = map_image
        self.level_data = data
        self.waypoints = []
        self.process_data()
        self.level = 1
        self.spawntime = 1200
        self.spawner: EnemySpawner = None
        self.enemyTypes = [EnemyType.happy, EnemyType.sad,
                           EnemyType.angry, EnemyType.suprise]

    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer['name'] == 'Path':
                for obj in layer['objects']:
                    waypoint_data = obj['polyline']
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data):
        for point in data:
            self.waypoints.append((point.get('x'), point.get('y') + 320))

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

    def get_spawn_time(self):
        return self.spawntime * math.pow(SPAWN_TIME_SCALER, float(self.level))

    def spawn(self):
        eType = self.enemyTypes[random.randint(0, 3)]
        return self.spawner.makeEnemy(eType, speed=SPEED_SCALER*self.level)

    # Check if score is heigh enough
    def updateLevel(self, score):
        self.level = int(score//SCORE_PER_LEVEL) + 1

    def set_spawner(self, spawner):
        self.spawner = spawner
