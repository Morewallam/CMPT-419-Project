# from game import TowerGame
from dataclasses import dataclass
import pygame
from gamestate import GameState
import constants as c
from enemy import Enemy
from spritesheet import Spritesheet


@dataclass
class GameLoop:
    game: 'TowerGame'  # type: ignore

    def handle_events(self):
        """
        Sample event handler that ensures quit events and normal
        event loop processing takes place. Without this, the game will
        hang, and repaints by the operating system will not happen,
        causing the game window to hang.
        """
        for event in pygame.event.get():
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ) or event.type == pygame.QUIT:
                self.set_state(GameState.quitting)
            # Delegate the event to a sub-event handler `handle_event`
            self.handle_event(event)

    def loop(self):
        while self.state != GameState.quitting:
            self.handle_events()

    def handle_event(self, event):
        """
        Handles a singular event, `event`.
        """

    # Convenient shortcuts.
    def set_state(self, new_state):
        self.game.set_state(new_state)

    @property
    def screen(self):
        return self.game.screen

    @property
    def state(self):
        return self.game.state


class GameMenu(GameLoop):
    def loop(self):
        clock = pygame.time.Clock()

        enemy = Enemy(self.game.image_sprites[(
            False, False, "black_dragon")], (200, 300))

        # create groups
        enemy_group = pygame.sprite.Group()
        enemy_group.add(enemy)
        tick = 0
        # self.screen.blit(
        #     self.game.image_sprites[(False, False, "black_dragon")], (0, 0))
        while self.state == GameState.main_menu:
            self.handle_events()
            self.screen.fill((50, 50, 50))
            enemy.move()
            enemy_group.draw(self.screen)

            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(c.DESIRED_FPS)


class GameEditing(GameLoop):
    pass
