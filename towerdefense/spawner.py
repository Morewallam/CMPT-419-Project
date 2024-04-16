from enemy import Enemy
from constants import EnemyType

'''
Spawns enemies
'''


class EnemySpawner():
    def __init__(self, sprites, waypoints, deathhandler, end_handler):
        self.sprites = sprites
        self.waypoints = waypoints
        self.deathhandler = deathhandler
        self.end_handler = end_handler

    def makeEnemy(self, type, speed=1):
        return Enemy(self.sprites, self.waypoints, type, self.deathhandler, self.end_handler, speed)
