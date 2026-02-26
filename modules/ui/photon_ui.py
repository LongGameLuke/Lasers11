# Main UI controller — initializes pygame, registers all scenes, and drives
# the per-frame event/update/render loop via the scene manager.

import pygame
from modules.ui.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from modules.ui.scene import SceneManager
from modules.ui.splash_screen import SplashScreen
from modules.ui.player_entry import PlayerEntry
from modules.ui.countdown import StartGame_Countdown
from modules.ui.game_action import GameAction
from modules.ui.network_config import NetworkConfig


class PhotonUI:
    def __init__(self, game):
        self.game = game

        # Initialize pygame and create the game window
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Photon Laser Tag")
        self.clock = pygame.time.Clock()

        # Set up the scene manager and register all our scenes
        self.scene_manager = SceneManager(game, self.screen)
        self.scene_manager.add("SPLASH", SplashScreen)
        self.scene_manager.add("PLAYER_ENTRY", PlayerEntry)
        self.scene_manager.add("NETWORK_CONFIG", NetworkConfig)
        self.scene_manager.add("COUNTDOWN_TIMER", StartGame_Countdown)
        self.scene_manager.add("GAME_ACTION", GameAction)

        # Start on the splash screen
        self.scene_manager.switch("SPLASH")

    def kill_pygame(self):
        """Clean up pygame when the game is shutting down."""
        pygame.quit()

    def update(self)->bool:
        """Called once per frame by PhotonGame.
        Handles window events, delegates to the current scene, and flips the display.
        Returns False if the user closed the window, True otherwise."""

        # Grab all pygame events this frame
        events = pygame.event.get()
        for event in events:
            # If the user clicked the X button, signal that we should quit
            if event.type == pygame.QUIT:
                return False

        # Let the current scene handle input, update its logic, and draw itself
        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.handle_events(events)
            self.scene_manager.current_scene.update()
            self.scene_manager.current_scene.render()

        # Push everything we drew to the actual screen and cap at 30 FPS
        pygame.display.flip()
        self.clock.tick(30)
        return True

