# Countdown scene — displays a countdown timer before the game begins.
# Transitions to GameAction once the countdown finishes.

import pygame
from modules.ui.scene import Scene
from modules.ui.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, WHITE, LIGHT_GREEN, HEADER_SIZE,
)


class StartGame_Countdown(Scene):
    def enter(self):
        self.font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE)
        self.countdown_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE + 40)

    def update(self):
        if not self.game.timer.active and not self.game.start_game_flag:
            self.manager.switch("GAME_ACTION")

    def render(self):
        self.screen.fill(BACKGROUND)
        self.draw_text(
            f"GAME IS STARTING IN:",
            self.font,
            WHITE,
            SCREEN_WIDTH//2,
            SCREEN_HEIGHT//3,
            center = True
        )

        self.draw_text(
            int(self.game.timer.time),
            self.countdown_font,
            LIGHT_GREEN,
            SCREEN_WIDTH//2,
            SCREEN_HEIGHT//2,
            center = True
        )

    def draw_text(self, text, font, color, x, y, center=False):
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)