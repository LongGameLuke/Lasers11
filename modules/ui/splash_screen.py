# Splash screen scene — displays the logo for 3 seconds before transitioning to player entry

import pygame
import time
from modules.ui.scene import Scene
from modules.ui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, HEADER_SIZE


class SplashScreen(Scene):
    def enter(self):
        font_cfg = self.game.config["photon"]["game"]["ui"]["fonts"]

        self.start_time = time.time()
        self.font = pygame.font.SysFont(None, HEADER_SIZE)

        # Loads and scales logo image
        self.image = None
        img = pygame.image.load("assets/images/logo.jpg")
        self.image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self):
        # Moves on to the player entry after 3 seconds
        if time.time() - self.start_time > 3:
            self.manager.switch("PLAYER_ENTRY")

    def render(self):
        # Draws logo image, but nothing else
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.image, (0, 0))
