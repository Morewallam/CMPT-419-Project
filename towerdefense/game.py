from dataclasses import dataclass, field
import pygame
from game_loops import GameLoop, GameMenu, GamePlaying, GameEnding
from gamestate import GameState, StateError
from file_import import import_image, import_sound
import constants as c


@dataclass
class TowerGame:

    game_menu: GameLoop = field(init=False, default=None)
    game_play: GameLoop = field(init=False, default=None)
    game_ending: GameLoop = field(init=False, default=None)
    screen: pygame.Surface
    size: tuple
    fullscreen: bool
    state: GameState
    channels: dict = field(init=False, default=None)
    image_sprites: dict = field(init=False, default=None)
    sounds: dict = field(init=False, default=None)
    score: int

    @classmethod
    def create(cls, size, fullscreen=False):
        game = cls(
            screen=None,
            size=size,
            fullscreen=fullscreen,
            state=GameState.initializing,
            score=0
        )
        game.init()
        return game

    def set_state(self, new_state):
        self.state = new_state

    def assert_state_is(self, *expected_states: GameState):
        """
        Asserts that the game engine is one of
        `expected_states`. If that assertions fails, raise
        `StateError`.
        """
        if not self.state in expected_states:
            raise StateError(
                f"Expected the game state to be one of {expected_states} not {self.state}"
            )

    def quit(self):
        pygame.quit()

    def start_game(self):
        self.assert_state_is(GameState.initialized)
        self.set_state(GameState.main_menu)
        self.loop()

    def loop(self):
        while self.state != GameState.quitting:
            if self.state == GameState.main_menu:
                self.game_menu.loop()
                # pass control to the game menu's loop
            elif self.state == GameState.game_playing:
                self.game_play.loop()
            elif self.state == GameState.game_ended:
                self.game_ending.loop()
        self.quit()

    def init(self):
        self.assert_state_is(GameState.initializing)
        pygame.init()
        window_style = pygame.FULLSCREEN if self.fullscreen else 0
        # We want 32 bits of color depth
        bit_depth = pygame.display.mode_ok(
            self.size, window_style, 32)
        screen = pygame.display.set_mode(
            self.size, window_style, bit_depth)
        pygame.mixer.pre_init(
            frequency=44100,
            size=32,
            # N.B.: 2 here means stereo, not the number of channels to
            # use in the mixer
            channels=2,
            buffer=512,
        )
        pygame.font.init()

        self.image_sprites = {}
        # Get the sprites for the game
        for sprite_index, sprite_name in c.SPRITES.items():
            img = import_image(sprite_name)
            for flipped_x in (True, False):
                for flipped_y in (True, False):
                    new_img = pygame.transform.flip(
                        img, flip_x=flipped_x, flip_y=flipped_y)
                    self.image_sprites[(flipped_x, flipped_y,
                                        sprite_index)] = new_img

        self.channels = {
            "enemies": None,
            "hit": None,
            "UI": None
        }
        # Get the channels for the game
        for channel_id, channel_name in enumerate(self.channels):
            self.channels[channel_name] = pygame.mixer.Channel(channel_id)
            # Configure the volume here.
            self.channels[channel_name].set_volume(1.0)
        self.channels["enemies"].set_volume(0.5)

        self.sounds = {}
        for index, name in c.SOUNDS.items():
            sound = import_sound(name)
            self.sounds[index] = sound

        self.screen = screen
        self.game_menu = GameMenu(game=self)
        self.game_play = GamePlaying(game=self)
        self.game_ending = GameEnding(game=self)
        self.set_state(GameState.initialized)
