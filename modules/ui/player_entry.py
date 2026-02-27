# Player entry scene — dual-team grid for entering player IDs, names, and equipment IDs.
# Supports keyboard navigation, mouse cell selection, and DB lookups for returning players.

import pygame
from modules.ui.scene import Scene
from modules.ui.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND, WHITE, RED, GREEN,
    YELLOW, LIGHT_GREEN, GRAY, FONT_SIZE, HEADER_SIZE, GRID_START_Y, ROW_HEIGHT,
    COL_WIDTH, MAX_TEAM_ROWS,
)


class PlayerEntry(Scene):
    def enter(self):
        # Set up our fonts
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.status_font = pygame.font.SysFont(None, HEADER_SIZE)
        self.header_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", 50)

        # Only initialize the grid data the first time we enter this scene.
        # If the player goes to network config and comes back, we want to keep their entries.
        if not hasattr(self, "red_entries"):
            # Each entry is [player_id, codename, equipment_id] as strings
            # Start with one empty row per team
            self.red_entries = [["", "", ""]]
            self.green_entries = [["", "", ""]]

            # Track which cell is currently selected
            self.current_team = "Red"
            self.current_row = 0
            self.current_col = 0

        # Status message shown at the bottom (success/error feedback)
        self.status_message = ""
        self.status_color = WHITE

    def handle_events(self, events):
        for event in events:
            # Left click — select whatever cell was clicked on
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                hit = self.hit_cell(mx, my)
                if hit:
                    team, row, col = hit
                    self.current_team = team
                    self.current_row = row
                    self.current_col = col

            elif event.type == pygame.KEYDOWN:
                # F5 — start the game (triggers countdown)
                if event.key == pygame.K_F5:
                    self.game.start_game_flag = True
                    self.manager.switch("COUNTDOWN_TIMER")
                # F7 — open network configuration
                elif event.key == pygame.K_F7:
                    self.manager.switch("NETWORK_CONFIG")
                # F12 — clear all player entries and reset
                elif event.key == pygame.K_F12:
                    self.clear_entries()
                    self.game.clear_players()
                # Enter — confirm/process the current cell's input
                elif event.key in [pygame.K_RETURN]:
                    self.process_input()
                # Backspace — delete last character in current cell
                elif event.key == pygame.K_BACKSPACE:
                    entries = self.get_entries(self.current_team)
                    curr_val = entries[self.current_row][self.current_col]
                    entries[self.current_row][self.current_col] = curr_val[:-1]

                # Arrow key navigation through the grid
                elif event.key == pygame.K_UP:
                    self.current_row = max(0, self.current_row - 1)
                elif event.key == pygame.K_DOWN:
                    entries = self.get_entries(self.current_team)
                    self.current_row = min(len(entries) - 1, self.current_row + 1)
                elif event.key == pygame.K_LEFT:
                    self.current_col = max(0, self.current_col - 1)
                elif event.key == pygame.K_RIGHT:
                    self.current_col = min(2, self.current_col + 1)

                # Any other printable character — type into the current cell
                else:
                    if event.unicode.isprintable():
                        entries = self.get_entries(self.current_team)
                        entries[self.current_row][self.current_col] += event.unicode

    def get_entries(self, team: str):
        """Return the entry list for the given team."""
        return self.red_entries if team == "Red" else self.green_entries

    def ensure_nex_row(self, team: str, row_completed_idx: int) -> None:
        """After a player is added, append a new empty row to the team's grid
        so the next player can be entered (up to MAX_TEAM_ROWS)."""
        entries = self.get_entries(team)
        if row_completed_idx == len(entries) - 1 and len(entries) < MAX_TEAM_ROWS:
            entries.append(["", "", ""])

    def hit_cell(self, mx: int, my: int):
        """Check if a mouse click landed on a grid cell.
        Returns (team, row, col) if a cell was hit, or None otherwise.
        We check both the Red pane (left side, starting at x=110) and
        the Green pane (right side, starting at x=750)."""
        panes = [("Red", 110, self.red_entries),("Green", 750, self.green_entries),]

        for team, base_x, entries in panes:
            rows = len(entries)
            if rows <= 0:
                continue

            # Check if the click Y is within this team's grid area
            top = GRID_START_Y
            bottom = GRID_START_Y + rows * ROW_HEIGHT

            if my < top or my > bottom:
                continue

            # Figure out which row was clicked
            row = (my - GRID_START_Y) // ROW_HEIGHT
            if row < 0 or row >= rows:
                continue

            # Check each of the 3 columns to see if the click is inside a cell
            for col in range(3):
                x = base_x + col * 150
                rect = pygame.Rect(x, GRID_START_Y + row * ROW_HEIGHT, COL_WIDTH, 25)
                if rect.collidepoint(mx, my):
                    return (team, int(row), int(col))

        return None

    def process_input(self):
        """Handle Enter key press on the currently selected cell.
        Behavior depends on which column we're in:
          Col 0 (Player ID): Look up the player in the DB, auto-fill name if found
          Col 1 (Code Name): Just move focus to the equipment ID column
          Col 2 (Equipment ID): Validate everything and add the player to the game"""
        team = self.current_team
        entries = self.get_entries(team)

        row = self.current_row
        col = self.current_col
        val = entries[row][col].strip()
        if not val: return

        # Column 0: Player ID field
        if col == 0:
            if val.isdigit():
                # Try to look up this player ID in the database
                try:
                    player = self.game.db.get_player_by_pid(int(val))
                    if player:
                        # Found them — auto-fill their name and skip to equipment ID
                        entries[row][1] = player[1]
                        self.current_col = 2
                        return
                    else:
                        # New player — move to name field so they can type it in
                        self.current_col = 1
                except: pass # Add db error handling
            else:
                self.status_message = "Player ID must be an integer!"
                self.status_color = RED

        # Column 1: Code Name field — just advance to equipment ID
        elif col == 1:
            self.current_col = 2

        # Column 2: Equipment ID field — validate and add the player
        elif col == 2:
            try:
                # Validate all three fields before we try to add the player
                test_pid = entries[row][0].strip()
                if not test_pid.isdigit():
                    raise ValueError("Player ID must be an integer")
                if not entries[row][1]:
                    raise ValueError("Name cannot be empty")
                if not val.isdigit():
                    raise ValueError("Equipment ID must be an integer")

                pid = int(entries[row][0])
                name = entries[row][1].strip()
                equipment_id = int(val)

                # add_new_player returns True if this is a brand new player, False if returning
                if self.game.add_new_player(pid, name, equipment_id, team):
                    self.status_message = f"Added {name} to {team} team!"
                else:
                    self.status_message = f"Loaded {name} into {team} team, welcome back!"
                self.status_color = GREEN

                # Add a new empty row so the next player can be entered
                self.ensure_nex_row(team, row)
                entries = self.get_entries(team)
                # Move cursor down to the new row, back to the first column
                if self.current_row < len(entries) - 1:
                    self.current_row += 1
                self.current_col = 0

            except Exception as e:
                self.status_message = str(e)
                self.status_color = RED

    def clear_entries(self):
        """Reset both team grids back to a single empty row each."""
        self.red_entries = [["", "", ""]]
        self.green_entries = [["", "", ""]]
        self.current_team = "Red"
        self.current_row = 0
        self.current_col = 0

    def render(self):
        self.screen.fill(BACKGROUND)

        # Draw team headers at the top
        self.draw_text("RED", self.header_font, RED,
                        SCREEN_WIDTH//4, 50, center=True)
        self.draw_text("GREEN", self.header_font, LIGHT_GREEN,
                        3*SCREEN_WIDTH//4, 50, center=True)

        # Draw column headers for both grids
        cols = ["Player ID", "Code Name", "Equipment ID"]
        for i, text in enumerate(cols):
            self.draw_text(text, self.font, WHITE, 135 + i*150, 95)   # Red side
            self.draw_text(text, self.font, WHITE, 775 + i*150, 95)   # Green side

        # Draw RED team rows (left side of screen)
        for r, row_vals in enumerate(self.red_entries):
            base_x = 110
            y = GRID_START_Y + r * ROW_HEIGHT
            # Row number label on the left
            self.draw_text(f"{r + 1:2}", self.font, GRAY, base_x - 35, y + 5)

            for c in range(3):
                x = base_x + c * 150
                rect = pygame.Rect(x, y, COL_WIDTH, 25)

                # Highlight the currently selected cell in yellow, others in gray
                if self.current_team == "Red" and r == self.current_row and c == self.current_col:
                    pygame.draw.rect(self.screen, YELLOW, rect, 2)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

                # Draw the text inside the cell if there's any
                val = row_vals[c]
                if val:
                    self.draw_text(val, self.font, WHITE, x + 5, y + 5)

        # Draw GREEN team rows (right side of screen)
        for r, row_vals in enumerate(self.green_entries):
            base_x = 750
            y = GRID_START_Y + r * ROW_HEIGHT
            self.draw_text(f"{r + 1:2}", self.font, GRAY, base_x - 35, y + 5)

            for c in range(3):
                x = base_x + c * 150
                rect = pygame.Rect(x, y, COL_WIDTH, 25)

                if self.current_team == "Green" and r == self.current_row and c == self.current_col:
                    pygame.draw.rect(self.screen, YELLOW, rect, 2)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

                val = row_vals[c]
                if val:
                    self.draw_text(val, self.font, WHITE, x + 5, y + 5)

        # Show status message near the bottom (tells the user what just happened)
        if self.status_message:
            self.draw_text (
                self.status_message,
                self.status_font,
                self.status_color,
                SCREEN_WIDTH//2,
                SCREEN_HEIGHT - 65,
                center=True
                )

        # Controls hint bar at the very bottom
        self.draw_text(
            "Enter: Save entry | F5: Start Game | F7: Network Config | F12: Clear Entries",
            self.font,
            YELLOW,
            SCREEN_WIDTH//2,
            SCREEN_HEIGHT - 30,
            center=True
            )

    def draw_text(self, text, font, color, x, y, center=False):
        """Helper to render text to the screen. If center=True, the text is
        centered on (x, y) instead of using it as the top-left corner."""
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)
