# Network configuration scene — allows editing the server host, broadcast port, and receive port.
# Changes are applied live to the game server when the user presses Enter.


import pygame
from modules.ui.scene import Scene
from modules.ui.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, WHITE, RED, GREEN,
    YELLOW, GRAY, FONT_SIZE, HEADER_SIZE,
)


class NetworkConfig(Scene):
    def enter(self):
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.header_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE)

        # Pull the current network settings from the server so the fields
        # show what's actually configured right now
        self.host = self.game.server.host
        self.broadcast_port = str(self.game.server.broadcast_port)
        self.receive_port = str(self.game.server.receive_port)

        # Which field is currently selected (0=host, 1=broadcast, 2=receive)
        self.current_field = 0

        # Status message for save confirmation or error feedback
        self.status_message = ""
        self.status_color = WHITE

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # F7 or ESC — go back to player entry
                if event.key == pygame.K_F7 or event.key == pygame.K_ESCAPE:
                    self.manager.switch("PLAYER_ENTRY")
                # Up/Down arrows — cycle through the 3 fields
                elif event.key == pygame.K_UP:
                    self.current_field = (self.current_field - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.current_field = (self.current_field + 1) % 3
                # Enter — save the current values to the server
                elif event.key == pygame.K_RETURN:
                    self.save_changes()
                # Backspace — delete last character from the selected field
                elif event.key == pygame.K_BACKSPACE:
                    if self.current_field == 0: self.host = self.host[:-1]
                    elif self.current_field == 1: self.broadcast_port = self.broadcast_port[:-1]
                    elif self.current_field == 2: self.receive_port = self.receive_port[:-1]
                # Any printable character — append to the selected field
                else:
                    if event.unicode.isprintable():
                        if self.current_field == 0: self.host += event.unicode
                        elif self.current_field == 1: self.broadcast_port += event.unicode
                        elif self.current_field == 2: self.receive_port += event.unicode

    def save_changes(self):
        """Push the edited values to the game server. Ports get converted to ints here,
        so if the user typed something that's not a number it'll get caught."""
        try:
            self.game.server.set_network(
                host=self.host.strip(),
                broadcast=int(self.broadcast_port),
                receive=int(self.receive_port)
            )
            self.status_message = "Network settings updated!"
            self.status_color = GREEN
        except Exception as e:
            self.status_message = f"Error: {e}"
            self.status_color = RED

    def render(self):
        self.screen.fill(BACKGROUND)

        # Title at the top
        self.draw_text("NETWORK CONFIGURATION", self.header_font, YELLOW,
                        SCREEN_WIDTH//2, 100, center=True)

        # The 3 editable fields with their labels and current values
        fields = [
            ("Host Address:", self.host),
            ("Broadcast Port:", self.broadcast_port),
            ("Receive Port:", self.receive_port)
        ]

        for i, (label, value) in enumerate(fields):
            y = 250 + i * 60

            # Draw the label text to the left
            self.draw_text(label, self.font, WHITE, SCREEN_WIDTH//2 - 200, y)

            # Draw the input box — yellow border if selected, gray otherwise
            rect = pygame.Rect(SCREEN_WIDTH//2, y - 5, 300, 30)
            if i == self.current_field:
                pygame.draw.rect(self.screen, YELLOW, rect, 2)
            else:
                pygame.draw.rect(self.screen, GRAY, rect, 1)

            # Draw the current value inside the box
            self.draw_text(value, self.font, WHITE, SCREEN_WIDTH//2 + 10, y)

        # Show save confirmation or error message
        if self.status_message:
            self.draw_text(self.status_message, self.font, self.status_color,
                            SCREEN_WIDTH//2, 450, center=True)

        # Controls hint at the bottom
        self.draw_text("Arrows: Move | Enter: Save | F7/ESC: Back",
                        self.font, GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, center=True)

    def draw_text(self, text, font, color, x, y, center=False):
        """Helper to render text to the screen."""
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)