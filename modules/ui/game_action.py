import pygame
from modules.ui.scene import Scene
from modules.ui.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, RED, LIGHT_GREEN, HEADER_SIZE, WHITE, YELLOW
)

class GameAction(Scene):
    def enter(self):
        self.font = pygame.font.SysFont(None, 32)
        self.status_font = pygame.font.SysFont(None, HEADER_SIZE)
        self.header_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", 70)
        self.label_font = pygame.font.SysFont(None, 24)
        self.player_font = pygame.font.SysFont(None, 28)
        self.score_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", 45)

    def render(self):
        self.screen.fill(BACKGROUND)

        margin = 30
        player_start_y = 100
        line_height = 38
        name_width = 220
        score_width = 70
        red_x = margin
        green_x = SCREEN_WIDTH - margin - name_width - score_width - 15

        # Draw Red title
        red_center_x = red_x + (name_width + score_width + 5) // 2
        self.draw_text("RED", self.header_font, RED, red_center_x, margin * 2, center=True)

        # Draw Green title
        green_center_x = green_x + (name_width + score_width + 5) // 2
        self.draw_text("GREEN", self.header_font, LIGHT_GREEN, green_center_x, margin * 2, center=True)

        # Score panes
        score_y = 150
        score_width_pane = 180
        score_height = 100
        score_gap = 40
        red_score_x = SCREEN_WIDTH // 2 - score_width_pane - score_gap // 2
        green_score_x = SCREEN_WIDTH // 2 + score_gap // 2

        # Red score pane
        self.draw_score_pane(red_score_x, score_y, score_width_pane, score_height, RED, "RED SCORE", self.game.get_team_score('Red'))

        # Green score pane
        self.draw_score_pane(green_score_x, score_y, score_width_pane, score_height, LIGHT_GREEN, "GREEN SCORE", self.game.get_team_score('Green'))

        # Separate players by team
        red_players = []
        green_players = []
        for p in self.game.players:
            if p.team == 'Red':
                red_players.append(p)
            elif p.team == 'Green':
                green_players.append(p)

        # Draw 15 static slots for each team
        self.draw_player_slots(red_players, red_x, RED, name_width, score_width, player_start_y, line_height)
        self.draw_player_slots(green_players, green_x, LIGHT_GREEN, name_width, score_width, player_start_y, line_height, flip=True)

        # Game events pane
        events_width = score_width_pane * 2 + score_gap
        events_x = red_score_x
        events_y = score_y + score_height + 40
        events_height = SCREEN_HEIGHT - events_y - margin
        pygame.draw.rect(self.screen, WHITE, (events_x, events_y, events_width, events_height), 3)
        self.draw_text("GAME EVENTS", self.label_font, WHITE, events_x + events_width // 2, events_y + 15, center=True)

        # Display 5 most recent events
        for i, e in enumerate(self.game.game_events[-5:]):
            y = events_y + (events_height // 3) + (i * 30)
            self.draw_text(str(e), self.status_font, YELLOW, events_x + events_width // 2, y, center=True)

    def draw_score_pane(self, x, y, w, h, color, label, score):
        pygame.draw.rect(self.screen, color, (x, y, w, h), 3)
        self.draw_text(label, self.label_font, WHITE, x + w // 2, y + 20, center=True)
        self.draw_text(str(score), self.score_font, color, x + w // 2, y + 60, center=True)

    def draw_player_slots(self, players, x, color, name_width, score_width, start_y, line_height, flip=False):
        if flip:
            w1, w2 = score_width, name_width
        else:
            w1, w2 = name_width, score_width

        for i in range(15):
            y = start_y + i * line_height
            x2 = x + w1 + 5
            pygame.draw.rect(self.screen, color, (x, y, w1, 35), 2)
            pygame.draw.rect(self.screen, color, (x2, y, w2, 35), 2)

            if i < len(players):
                p = players[i]
                if flip:
                    t1, t2 = str(p.score), p.name
                else:
                    t1, t2 = p.name, str(p.score)
                self.draw_text(t1, self.player_font, color, x + w1 // 2, y + 17, center=True)
                self.draw_text(t2, self.player_font, color, x2 + w2 // 2, y + 17, center=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5 or event.key == pygame.K_ESCAPE:
                    self.manager.switch("PLAYER_ENTRY")

    def draw_text(self, text, font, color, x, y, center=False):
        """Helper to render text to the screen."""
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)