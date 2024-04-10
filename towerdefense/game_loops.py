# from game import TowerGame
from dataclasses import dataclass
import pygame
from gamestate import GameState
import constants as c
from enemy import Enemy
from spritesheet import Spritesheet
from world import World
import json
from button import Button
from constants import EnemyType
from spawner import EnemySpawner


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


class GamePlaying(GameLoop):

    def loop(self):
        clock = pygame.time.Clock()
        # load json data for level

        last_spawn_time = pygame.time.get_ticks()
        self.game.score = 0

        enemy_types_images = {
            EnemyType.happy: self.game.image_sprites[(
                False, False, "yellow_dragon")],
            EnemyType.sad: self.game.image_sprites[(
                False, False, "blue_dragon")],
            EnemyType.angry: self.game.image_sprites[(
                False, False, "red_dragon")],
            EnemyType.suprise: self.game.image_sprites[(
                False, False, "black_dragon")],
        }

        uiss = Spritesheet(self.game.image_sprites[(
            False, False, "ui_elements")])
        button_imgs = uiss.load_strip((0, 8*16, 16, 16), 4, -1)

        hit_sound = self.game.sounds['hit']
        jump_sound = self.game.sounds['jump']
        end_sound = self.game.sounds['end']

        with open('towerdefense/assests/levels/Map.tmj') as file:
            world_data = json.load(file)

        enemy_group = pygame.sprite.Group()

        def death_handler():
            self.game.channels['hit'].play(hit_sound)
            self.game.score += 1

        def end_handler():
            self.game.channels['enemies'].play(
                end_sound, fade_ms=500)
            self.game.channels['enemies'].fadeout(500)

            self.set_state(GameState.game_ended)

        world = World(world_data, self.game.image_sprites[(
            False, False, "map")])

        spawner = EnemySpawner(
            enemy_types_images, world.waypoints, death_handler, end_handler)

        world.set_spawner(spawner)

        def button_handler(type):
            def handler():
                enemy_sprites = enemy_group.sprites()
                for enemy in enemy_sprites:
                    if enemy.get_type() == type:
                        enemy.kill()
            return handler

        smile_btn = Button(c.WIDTH + 10, 10, button_imgs[3],
                           button_handler(EnemyType.happy))
        angry_btn = Button(c.WIDTH + 64+20, 10, button_imgs[0],
                           button_handler(EnemyType.angry))
        sad_btn = Button(c.WIDTH + 10, 64+10+20, button_imgs[1],
                         button_handler(EnemyType.sad))
        suprise_btn = Button(c.WIDTH + 64+20, 64+10+20, button_imgs[2],
                             button_handler(EnemyType.suprise))
        font = pygame.font.Font(pygame.font.get_default_font(), 32)

        while self.state == GameState.game_playing:
            self.handle_events()
            self.screen.fill((50, 50, 50))
            world.draw(self.screen)
            smile_btn.draw(self.screen)
            angry_btn.draw(self.screen)
            sad_btn.draw(self.screen)
            suprise_btn.draw(self.screen)

            # perform updates for all enemies in group
            enemy_group.update()

            # Draw all of the sprites to the screen
            enemy_group.draw(self.screen)

            if pygame.time.get_ticks() - last_spawn_time > int(world.get_spawn_time()):
                enemy_group.add(world.spawn())
                self.game.channels['enemies'].play(jump_sound)
                last_spawn_time = pygame.time.get_ticks()

            world.updateLevel(self.game.score)
            score_text = font.render(
                f'Score:{self.game.score}', True, (255, 255, 255))
            level_text = font.render(
                f'Level:{world.level}', True, (255, 255, 255))
            self.screen.blit(score_text, (c.WIDTH, c.HEIGHT//2))
            self.screen.blit(level_text, (c.WIDTH, c.HEIGHT//2 + 30))

            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(c.DESIRED_FPS)


class GameEnding(GameLoop):
    def loop(self):
        clock = pygame.time.Clock()
        font = pygame.font.Font(pygame.font.get_default_font(), 32)

        score_text = font.render(
            f'You got a score of {self.game.score}', True, (255, 255, 255))

        play_text = font.render(
            'Play Again!', True, (255, 255, 255))
        menu_text = font.render(
            'Main Menu', True, (255, 255, 255))
        quit_text = font.render(
            "Quit", True, (255, 255, 255))

        confirm = self.game.sounds['confirm']
        cancel = self.game.sounds['cancel']

        def play_handler():
            self.game.channels['UI'].play(confirm)
            self.set_state(GameState.game_playing)

        def quit_handler():
            self.game.channels['UI'].play(cancel)
            self.set_state(GameState.quitting)

        def menu_handler():
            self.game.channels['UI'].play(confirm)
            self.set_state(GameState.main_menu)

        play_btn = Button((c.WIDTH + c.SIDE_PANEL)//2, c.HEIGHT//2,
                          play_text, play_handler, center=True)

        quit_btn = Button((c.WIDTH + c.SIDE_PANEL)//2, c.HEIGHT//2 + 200,
                          quit_text, quit_handler, center=True)

        menu_btn = Button((c.WIDTH + c.SIDE_PANEL)//2, c.HEIGHT//2 + 50,
                          menu_text, menu_handler, center=True)

        rect = score_text.get_rect()
        rect.center = ((c.WIDTH + c.SIDE_PANEL)//2, c.HEIGHT//2 - 100)

        while self.state == GameState.game_ended:
            self.handle_events()

            self.screen.fill((50, 50, 50))

            self.screen.blit(
                score_text, rect)
            play_btn.draw(self.screen)
            quit_btn.draw(self.screen)
            menu_btn.draw(self.screen)

            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(c.DESIRED_FPS)


class GameMenu(GameLoop):
    def loop(self):
        clock = pygame.time.Clock()

        font = pygame.font.Font(pygame.font.get_default_font(), 32)
        play_text = font.render(
            'Play', True, (255, 255, 255))
        quit_text = font.render(
            "Quit", True, (255, 255, 255))

        confirm = self.game.sounds['confirm']
        cancel = self.game.sounds['cancel']

        def play_handler():
            self.game.channels['UI'].play(confirm)
            self.set_state(GameState.game_playing)

        def quit_handler():
            self.game.channels['UI'].play(cancel)
            self.set_state(GameState.quitting)

        play_btn = Button((c.WIDTH + c.SIDE_PANEL)//2, c.HEIGHT//2,
                          play_text, play_handler, center=True)

        quit_btn = Button((c.WIDTH + c.SIDE_PANEL)//2, c.HEIGHT//2 + 200,
                          quit_text, quit_handler, center=True)

        while self.state == GameState.main_menu:
            self.handle_events()

            self.screen.fill((50, 50, 50))

            play_btn.draw(self.screen)
            quit_btn.draw(self.screen)

            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(c.DESIRED_FPS)
