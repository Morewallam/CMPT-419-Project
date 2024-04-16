'''
All the Classes that perform the game loops for different stages of the game
'''
# from game import TowerGame
from dataclasses import dataclass
import cv2
import numpy as np
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
import threading


@dataclass
class GameLoop:
    '''
    Base class for functionality of each game loop
    '''
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

    '''
    Game loop that handles playing the game
    '''

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

        font = pygame.font.Font(pygame.font.get_default_font(), 32)

        ret, frame = self.game.camera.read()
        self.current_image = frame

        self.getting_image = False
        self.current_emotion = None

        def hitEnemy(emotion):
            if emotion:
                enemy_sprites = enemy_group.sprites()
                for enemy in enemy_sprites:
                    if enemy.get_type() == emotion:
                        enemy.kill()

        def getImage():
            ret, frame = self.game.camera.read()
            if ret:
                self.game.model.find_face(frame)
                self.current_emotion = self.game.model.predict()
                self.current_image = self.game.model.draw_rec_with_label(frame)

            self.getting_image = False

        while self.state == GameState.game_playing:
            self.handle_events()
            self.screen.fill((50, 50, 50))
            world.draw(self.screen)

            frame = self.current_image

            if not self.getting_image:
                self.getting_image = True
                imageThread = threading.Thread(target=getImage)
                imageThread.start()

            hitEnemy(self.current_emotion)

            # perform updates for all enemies in group
            enemy_group.update()

            # Draw all of the sprites to the screen
            enemy_group.draw(self.screen)

            # Check if enough time has passed to spawn a new enemy
            if pygame.time.get_ticks() - last_spawn_time > int(world.get_spawn_time()):
                enemy_group.add(world.spawn())
                self.game.channels['enemies'].play(jump_sound)
                last_spawn_time = pygame.time.get_ticks()

            world.updateLevel(self.game.score)
            score_text = font.render(
                f'Score: {self.game.score}', True, (255, 255, 255))
            level_text = font.render(
                f'Level: {world.level}', True, (255, 255, 255))
            if self.current_emotion:
                emotion_text = font.render(
                    f'{self.current_emotion.value}', True, (255, 255, 255))
            else:
                emotion_text = font.render(
                    f'None', True, (255, 255, 255))

            frame = cv2.resize(frame, (c.SIDE_PANEL, 150))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(
                frame, (c.WIDTH, c.HEIGHT-frame.get_height()))

            self.screen.blit(emotion_text, (c.WIDTH, c.HEIGHT//2 + 70))
            self.screen.blit(score_text, (c.WIDTH, c.HEIGHT//2))
            self.screen.blit(level_text, (c.WIDTH, c.HEIGHT//2 + 30))

            # Black
            pygame.draw.rect(self.screen, (0, 0, 0),
                             pygame.Rect(c.WIDTH+10, 10, 32, 32))

            suprise_text = font.render(
                f'Suprise', True, (255, 255, 255))
            self.screen.blit(suprise_text, (c.WIDTH+52, 10))

            # Red
            pygame.draw.rect(self.screen, (255, 0, 0),
                             pygame.Rect(c.WIDTH+10, 42+10, 32, 32))

            anger_text = font.render(
                f'Angry', True, (255, 255, 255))
            self.screen.blit(anger_text, (c.WIDTH+52, 42+10))

            # Blue
            pygame.draw.rect(self.screen, (0, 0, 255),
                             pygame.Rect(c.WIDTH+10, 94, 32, 32))
            sad_text = font.render(
                f'Sad', True, (255, 255, 255))
            self.screen.blit(sad_text, (c.WIDTH+52, 94))
            # Yellow
            pygame.draw.rect(self.screen, (255, 255, 0),
                             pygame.Rect(c.WIDTH+10, 136, 32, 32))
            happy_text = font.render(
                f'Happy', True, (255, 255, 255))
            self.screen.blit(happy_text, (c.WIDTH+52, 136))

            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(c.DESIRED_FPS)


class GameEnding(GameLoop):
    '''
    Loop for game ending
    '''

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

        ret, frame = self.game.camera.read()
        self.current_image = frame

        self.getting_image = False

        def getImage():
            ret, frame = self.game.camera.read()
            if ret:
                self.game.model.find_face(frame)
                self.game.model.predict()
                self.current_image = self.game.model.draw_rec_with_label(frame)

            self.getting_image = False

        while self.state == GameState.game_ended:
            self.handle_events()

            self.screen.fill((50, 50, 50))

            self.screen.blit(
                score_text, rect)
            play_btn.draw(self.screen)
            quit_btn.draw(self.screen)
            menu_btn.draw(self.screen)

            frame = self.current_image

            if not self.getting_image:
                self.getting_image = True
                imageThread = threading.Thread(target=getImage)
                imageThread.start()

            frame = cv2.resize(frame, (c.SIDE_PANEL, 150))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(
                frame, (c.WIDTH, c.HEIGHT-frame.get_height()))

            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(c.DESIRED_FPS)


class GameMenu(GameLoop):
    '''
    Loop for the menu
    '''

    def loop(self):
        clock = pygame.time.Clock()

        font = pygame.font.Font(pygame.font.get_default_font(), 32)
        play_text = font.render(
            'Play', True, (255, 255, 255))
        quit_text = font.render(
            "Quit", True, (255, 255, 255))

        ret, frame = self.game.camera.read()
        self.current_image = frame

        self.getting_image = False

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

        def getImage():
            ret, frame = self.game.camera.read()
            if ret:
                self.game.model.find_face(frame)
                self.game.model.predict()
                self.current_image = self.game.model.draw_rec_with_label(frame)

            self.getting_image = False

        while self.state == GameState.main_menu:
            self.handle_events()

            self.screen.fill((50, 50, 50))

            frame = self.current_image

            if not self.getting_image:
                self.getting_image = True
                imageThread = threading.Thread(target=getImage)
                imageThread.start()

            # if pygame.time.get_ticks() % skip_frames == 0:
            #     self.game.model.find_face(frame)

            frame = cv2.resize(frame, (c.SIDE_PANEL, 150))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(
                frame, (c.WIDTH, c.HEIGHT-frame.get_height()))

            play_btn.draw(self.screen)
            quit_btn.draw(self.screen)

            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(c.DESIRED_FPS)
