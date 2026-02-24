import pygame
import sys
import time
import os
import socket


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (139, 0, 0)
GREEN = (0, 100, 0)
LIGHT_GREEN = (130, 255, 76)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

FONT_SIZE = 24
HEADER_SIZE = 36
GRID_START_Y = 120
ROW_HEIGHT = 30
COL_WIDTH = 140
MAX_TEAM_ROWS = 15

class Scene:
    def __init__(self, manager):
        self.manager = manager
        self.game = manager.game
        self.screen = manager.screen

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self):
        pass

class SceneManager:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.scenes = {}
        self.current_scene = None

    def add(self, name, scene_cls):
        self.scenes[name] = scene_cls(self)

    def switch(self, name):
        if self.current_scene:
            self.current_scene.exit()
        self.current_scene = self.scenes.get(name)
        if self.current_scene:
            self.current_scene.enter()

class SplashScreen(Scene):
    def enter(self):
        self.start_time = time.time()
        self.font = pygame.font.SysFont("Arial", HEADER_SIZE)
        
        self.image = None
        img = pygame.image.load("assets/images/logo.jpg")
        self.image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
    def update(self):
        if time.time() - self.start_time > 3:
            self.manager.switch("PLAYER_ENTRY")

    def render(self):
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.image, (0, 0))

class PlayerEntry(Scene):
    def enter(self):
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.status_font = pygame.font.SysFont(None, HEADER_SIZE)
        self.header_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE)
        
        # Initialize grid data if not already present (preserves data if returning)
        if not hasattr(self, "red_entries"):
            # Dynamic rows starting with 1 on each side.
            self.red_entries = [["", "", ""]]
            self.green_entries = [["", "", ""]]

            self.current_team = "Red"
            self.current_row = 0
            self.current_col = 0
        
        self.status_message = ""
        self.status_color = WHITE

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                hit = self.hit_cell(mx, my)
                if hit:
                    team, row, col = hit
                    self.current_team = team
                    self.current_row = row
                    self.current_col = col

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.game.start_game_flag = True
                    self.manager.switch("COUNTDOWN_TIMER")
                elif event.key == pygame.K_F7:
                    self.manager.switch("NETWORK_CONFIG")
                elif event.key == pygame.K_F12:
                    self.clear_entries()
                    self.game.clear_players()
                elif event.key in [pygame.K_RETURN]:
                    self.process_input()
                elif event.key == pygame.K_BACKSPACE:
                    entries = self.get_entries(self.current_team)
                    curr_val = entries[self.current_row][self.current_col]
                    entries[self.current_row][self.current_col] = curr_val[:-1]
                
                # Arrowkeys navigation
                elif event.key == pygame.K_UP:
                    self.current_row = max(0, self.current_row - 1)
                elif event.key == pygame.K_DOWN:
                    entries = self.get_entries(self.current_team)
                    self.current_row = min(len(entries) - 1, self.current_row + 1)
                elif event.key == pygame.K_LEFT:
                    self.current_col = max(0, self.current_col - 1)
                elif event.key == pygame.K_RIGHT:
                    self.current_col = min(2, self.current_col + 1)
                
                else:
                    if event.unicode.isprintable():
                        entries = self.get_entries(self.current_team)
                        entries[self.current_row][self.current_col] += event.unicode

    def get_entries(self, team: str):
        return self.red_entries if team == "Red" else self.green_entries

    def ensure_nex_row(self, team: str, row_completed_idx: int) -> None:
        """Append next row"""
        entries = self.get_entries(team)
        if row_completed_idx == len(entries) - 1 and len(entries) < MAX_TEAM_ROWS:
            entries.append(["", "", ""])

    def hit_cell(self, mx: int, my: int):
        panes = [("Red", 110, self.red_entries),("Green", 750, self.green_entries),]

        for team, base_x, entries in panes:
            rows = len(entries)
            if rows <= 0:
                continue

            top = GRID_START_Y
            bottom = GRID_START_Y + rows * ROW_HEIGHT

            if my < top or my > bottom:
                continue

            row = (my - GRID_START_Y) // ROW_HEIGHT
            if row < 0 or row >= rows:
                continue

            for col in range(3):
                x = base_x + col * 150
                rect = pygame.Rect(x, GRID_START_Y + row * ROW_HEIGHT, COL_WIDTH, 25)
                if rect.collidepoint(mx, my):
                    return (team, int(row), int(col))

        return None

    def process_input(self):
        team = self.current_team
        entries = self.get_entries(team)

        row = self.current_row
        col = self.current_col
        val = entries[row][col].strip()
        if not val: return

        # 1. PID Field
        if col == 0:
            if val.isdigit():
                # Query DB for existing player
                try:
                    player = self.game.db.get_player_by_pid(int(val))
                    if player:
                        entries[row][1] = player[1]
                        self.current_col = 2
                        return
                    else:
                        self.current_col = 1
                except: pass # Add db error handling        
            else:
                self.status_message = "Player ID must be an integer!"
                self.status_color = RED

        # 2. Name Field
        elif col == 1:
            self.current_col = 2
            
        elif col == 2:
            try:
                # Make sure finalized player entry is valid before adding to game
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
                
                if self.game.add_new_player(pid, name, equipment_id, team):
                    self.status_message = f"Added {name} to {team} team!"
                else:
                    self.status_message = f"Loaded {name} into {team} team, welcome back!"
                self.status_color = GREEN
                
                # Add a new row for team with freshly added entry
                self.ensure_nex_row(team, row)
                entries = self.get_entries(team)
                if self.current_row < len(entries) - 1:
                    self.current_row += 1
                self.current_col = 0

            except Exception as e:
                self.status_message = str(e)
                self.status_color = RED

    def clear_entries(self):
        self.red_entries = [["", "", ""]]
        self.green_entries = [["", "", ""]]
        self.current_team = "Red"
        self.current_row = 0
        self.current_col = 0

    def render(self):
        self.screen.fill(BACKGROUND)
        self.draw_text("RED TEAM", self.header_font, RED, 
                        SCREEN_WIDTH//4, 50, center=True)
        self.draw_text("GREEN TEAM", self.header_font, GREEN, 
                        3*SCREEN_WIDTH//4, 50, center=True)
        
        cols = ["Player ID", "Code Name", "Equipment ID"]
        for i, text in enumerate(cols):
            self.draw_text(text, self.font, WHITE, 135 + i*150, 95)
            self.draw_text(text, self.font, WHITE, 775 + i*150, 95)

        # Draw RED rows
        for r, row_vals in enumerate(self.red_entries):
            base_x = 110
            y = GRID_START_Y + r * ROW_HEIGHT
            self.draw_text(f"{r + 1:2}", self.font, GRAY, base_x - 35, y + 5)

            for c in range(3):
                x = base_x + c * 150
                rect = pygame.Rect(x, y, COL_WIDTH, 25)

                if self.current_team == "Red" and r == self.current_row and c == self.current_col:
                    pygame.draw.rect(self.screen, YELLOW, rect, 2)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

                val = row_vals[c]
                if val:
                    self.draw_text(val, self.font, WHITE, x + 5, y + 5)

        # Draw GREEN rows
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

        
        if self.status_message:
            self.draw_text (
                self.status_message, 
                self.status_font,
                self.status_color, 
                SCREEN_WIDTH//2, 
                SCREEN_HEIGHT - 65, 
                center=True
                )    

        self.draw_text(
            "Enter: Save entry | F5: Start Game | F7: Network Config | F12: Clear Entries", 
            self.font, 
            YELLOW, 
            SCREEN_WIDTH//2, 
            SCREEN_HEIGHT - 30, 
            center=True
            )

    def draw_text(self, text, font, color, x, y, center=False):
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)

class StartGame_Countdown(Scene):
    def enter(self):
        self.font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE)
        self.countdown_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE + 40)

    def update(self):
        if not self.game.countdown_active and not self.game.start_game_flag:
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
            int(self.game.countdown_time),
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

class GameAction(Scene):
    def enter(self):
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.status_font = pygame.font.SysFont(None, HEADER_SIZE)
        self.header_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE)

        self.image = None
        img = pygame.image.load("assets/images/logo.jpg")
        self.image = pygame.transform.scale(img, (200, 200))

    def render(self):
        self.screen.fill(BACKGROUND)
        self.screen.blit(self.image, (10, 10))
        self.draw_text("GAME ON!", self.header_font, LIGHT_GREEN, 
                        SCREEN_WIDTH//2, 100, center=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5 or event.key == pygame.K_ESCAPE:
                    self.manager.switch("PLAYER_ENTRY")
                else:
                    pass

    def draw_text(self, text, font, color, x, y, center=False):
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)

class NetworkConfig(Scene):
    def enter(self):
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.header_font = pygame.font.Font("assets/fonts/Orbitron/static/Orbitron-Bold.ttf", HEADER_SIZE)
        
        # Initialize with current values
        self.host = self.game.server.host
        self.broadcast_port = str(self.game.server.broadcast_port)
        self.receive_port = str(self.game.server.receive_port)

        # Fields: 0=host, 1=broadcast, 2=receive
        self.current_field = 0
        
        self.status_message = ""
        self.status_color = WHITE

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F7 or event.key == pygame.K_ESCAPE:
                    self.manager.switch("PLAYER_ENTRY")
                elif event.key == pygame.K_UP:
                    self.current_field = (self.current_field - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.current_field = (self.current_field + 1) % 3
                elif event.key == pygame.K_RETURN:
                    self.save_changes()
                elif event.key == pygame.K_BACKSPACE:
                    if self.current_field == 0: self.host = self.host[:-1]
                    elif self.current_field == 1: self.broadcast_port = self.broadcast_port[:-1]
                    elif self.current_field == 2: self.receive_port = self.receive_port[:-1]
                else:
                    if event.unicode.isprintable():
                        if self.current_field == 0: self.host += event.unicode
                        elif self.current_field == 1: self.broadcast_port += event.unicode
                        elif self.current_field == 2: self.receive_port += event.unicode

    def save_changes(self):
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
        self.draw_text("NETWORK CONFIGURATION", self.header_font, YELLOW, 
                        SCREEN_WIDTH//2, 100, center=True)
        
        fields = [
            ("Host Address:", self.host),
            ("Broadcast Port:", self.broadcast_port),
            ("Receive Port:", self.receive_port)
        ]

        for i, (label, value) in enumerate(fields):
            y = 250 + i * 60
            # Draw label
            self.draw_text(label, self.font, WHITE, SCREEN_WIDTH//2 - 200, y)
            
            # Draw field box
            rect = pygame.Rect(SCREEN_WIDTH//2, y - 5, 300, 30)
            if i == self.current_field:
                pygame.draw.rect(self.screen, YELLOW, rect, 2)
            else:
                pygame.draw.rect(self.screen, GRAY, rect, 1)
            
            # Draw value
            self.draw_text(value, self.font, WHITE, SCREEN_WIDTH//2 + 10, y)

        if self.status_message:
            self.draw_text(self.status_message, self.font, self.status_color, 
                            SCREEN_WIDTH//2, 450, center=True)

        self.draw_text("Arrows: Move | Enter: Save | F7/ESC: Back", 
                        self.font, GRAY, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, center=True)

    def draw_text(self, text, font, color, x, y, center=False):
        surf = font.render(str(text), True, color)
        rect = surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surf, rect)

class PhotonUI:
    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Photon Laser Tag")
        self.clock = pygame.time.Clock()

        self.scene_manager = SceneManager(game, self.screen)
        self.scene_manager.add("SPLASH", SplashScreen)
        self.scene_manager.add("PLAYER_ENTRY", PlayerEntry)
        self.scene_manager.add("NETWORK_CONFIG", NetworkConfig)
        self.scene_manager.add("COUNTDOWN_TIMER", StartGame_Countdown)
        self.scene_manager.add("GAME_ACTION", GameAction)
        self.scene_manager.switch("SPLASH")

    def kill_pygame(self):
        pygame.quit()

    def update(self)->bool:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
        
        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.handle_events(events)
            self.scene_manager.current_scene.update()
            self.scene_manager.current_scene.render()
        
        pygame.display.flip()
        self.clock.tick(30)
        return True