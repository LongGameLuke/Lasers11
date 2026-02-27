import pygame
from modules.ui.scene import Scene
from modules.ui.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, RED, LIGHT_GREEN, FONT_SIZE, HEADER_SIZE, WHITE
)


class GameAction(Scene):
    def enter(self):
        # Set up fonts — slightly bigger than default for readability during gameplay
        self.font = pygame.font.SysFont(None, 32)
        self.status_font = pygame.font.SysFont(None, HEADER_SIZE)
        self.header_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE)

    def render(self):
        self.screen.fill(BACKGROUND)

        # Team headers — Red on the left quarter, Green on the right quarter
        self.draw_text(
            f"RED TEAM  -  {self.game.red_team_score}", 
            self.header_font, 
            RED,
            SCREEN_WIDTH//4,
            100,
            center=True
            )

        self.draw_text(
            f"GREEN TEAM  -  {self.game.green_team_score}", 
            self.header_font, 
            LIGHT_GREEN,
            3*SCREEN_WIDTH//4,
            100, 
            center=True
            )

        # Starting position and spacing for the player name lists
        start_y = 150
        line_spacing = 35

        # Track Y positions separately since teams might have different player counts
        red_y = start_y
        green_y = start_y

        # Loop through all players and draw their names under the right team
        for p in self.game.players:
            if p.team == 'Red':
                self.draw_text(
                    f"{p.name}  -  {p.score}",
                    self.font,
                    RED,
                    SCREEN_WIDTH//4,
                    red_y,
                    center=True
                )
                red_y += line_spacing
            else:
                self.draw_text(
                    f"{p.name}  -  {p.score}",
                    self.font,
                    LIGHT_GREEN,
                    3*SCREEN_WIDTH//4,
                    green_y,
                    center=True
                )
                green_y += line_spacing

        # Draw the game events box at the bottom center of the screen
        box_width = SCREEN_WIDTH // 3
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT // 2)
        box_height = (SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 3)

        # Display 5 most recent events
        events = self.game.game_events[-5:]
        for i in range(len(events)):
            e = events[i]
            y = box_y + 100 + (i * 30)
            self.draw_text(
                str(e),
                self.status_font,
                WHITE, 
                SCREEN_WIDTH // 2, 
                y, 
                center=True
                )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # F5 or ESC — go back to player entry (ends the current game view)
                if event.key == pygame.K_F5 or event.key == pygame.K_ESCAPE:
                    self.manager.switch("PLAYER_ENTRY")
                else:
                    pass

    def draw_text(self, text, font, color, x, y, center=False):
        """Helper to render text to the screen."""
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)