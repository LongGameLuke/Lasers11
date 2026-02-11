import pygame
import sys
import time
import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (139, 0, 0)
GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

FONT_SIZE = 24
HEADER_SIZE = 36
GRID_START_Y = 120
ROW_HEIGHT = 30
COL_WIDTH = 140

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
        if not hasattr(self, 'entries'):
            # 30 rows, 3 columns: [PID, Name, Equipment ID]
            self.entries = [[ "", "", "" ] for _ in range(30)]
            self.current_row = 0
            self.current_col = 0
        
        self.status_message = ""
        self.status_color = WHITE

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.game.start_game()
                    self.manager.switch("GAME_ACTION")
                elif event.key == pygame.K_F12:
                    self.clear_entries()
                    self.game.clear_players()
                elif event.key in [pygame.K_RETURN]:
                    self.process_input()
                elif event.key == pygame.K_BACKSPACE:
                    curr_val = self.entries[self.current_row][self.current_col]
                    self.entries[self.current_row][self.current_col] = curr_val[:-1]
                
                # Arrowkeys navigation
                elif event.key == pygame.K_UP:
                    self.current_row = max(0, self.current_row - 1)
                elif event.key == pygame.K_DOWN:
                    self.current_row = min(29, self.current_row + 1)
                elif event.key == pygame.K_LEFT:
                    self.current_col = max(0, self.current_col - 1)
                elif event.key == pygame.K_RIGHT:
                    self.current_col = min(2, self.current_col + 1)
                
                else:
                    if event.unicode.isprintable():
                        self.entries[self.current_row][self.current_col] += event.unicode

    def process_input(self):
        row = self.current_row
        col = self.current_col
        val = self.entries[row][col].strip()
        if not val: return

        # 1. PID Field
        if col == 0:
            if val.isdigit():
                # Query DB for existing player
                try:
                    player = self.game.db.get_player_by_pid(int(val))
                    if player:
                        self.entries[row][1] = player[1]
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
                if not self.entries[row][0].isdigit(): 
                    raise ValueError("Player ID must be an integer")
                if not self.entries[row][1]: 
                    raise ValueError("Name cannot be empty")
                if not val.isdigit(): 
                    raise ValueError("Equipment ID must be an integer")
                
                pid = int(self.entries[row][0])
                name = self.entries[row][1]
                equipment_id = int(val)
                team = "Red" if row < 15 else "Green"
                
                if self.game.add_new_player(pid, name, equipment_id, team):
                    self.status_message = f"Added {name} to {team} team!"
                else:
                    self.status_message = f"Loaded {name} into {team} team, welcome back!"
                self.status_color = GREEN
                
                # Advance to next row
                if self.current_row < 29:
                    self.current_row += 1
                    self.current_col = 0

            except Exception as e:
                self.status_message = str(e)
                self.status_color = RED

    def clear_entries(self):
        self.entries = [[ "", "", "" ] for _ in range(30)]
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

        for r in range(30):
            is_green = r >= 15
            display_r = r - 15 if is_green else r
            base_x = 750 if is_green else 110
            y = GRID_START_Y + display_r * ROW_HEIGHT
            self.draw_text(f"{display_r + 1:2}", self.font, GRAY, base_x - 35, y + 5)
            
            for c in range(3):
                x = base_x + c * 150
                rect = pygame.Rect(x, y, COL_WIDTH, 25)
                
                # Focus on current selection
                if r == self.current_row and c == self.current_col:
                    pygame.draw.rect(self.screen, YELLOW, rect, 2)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)
                
                val = self.entries[r][c]
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
            "Arrow Keys: Navigate | Enter: Save entry | F5: Start Game | F12: Clear Entries", 
            self.font, 
            GRAY, 
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

class GameAction(Scene):
    def enter(self):
        pass

class PhotonUI:
    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Photon Laser Tag")

        self.scene_manager = SceneManager(game, self.screen)
        self.scene_manager.add("SPLASH", SplashScreen)
        self.scene_manager.add("PLAYER_ENTRY", PlayerEntry)
        self.scene_manager.add("GAME_ACTION", GameAction)
        self.scene_manager.switch("SPLASH")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            if self.scene_manager.current_scene:
                self.scene_manager.current_scene.handle_events(events)
                self.scene_manager.current_scene.update()
                self.scene_manager.current_scene.render()
            
            pygame.display.flip()
            clock.tick(30)
        
        pygame.quit()
        sys.exit()