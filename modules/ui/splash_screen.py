import pygame
import time
from modules.ui.scene import Scene
from modules.ui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, HEADER_SIZE


class SplashScreen(Scene):
    def enter(self):
        font_cfg = self.game.config["photon"]["game"]["ui"]["fonts"]

        self.start_time = time.time()
        self.font = pygame.font.SysFont(None, HEADER_SIZE)

        self.image = None
        img = pygame.image.load("assets/images/logo.jpg")
        self.image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self):
        if time.time() - self.start_time > 3:
            self.manager.switch("PLAYER_ENTRY")

    def render(self):
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.image, (0, 0))
