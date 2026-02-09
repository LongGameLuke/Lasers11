import pygame
import sys

class PhotonUI:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Photon Laser Tag")
        
        self.colors = {
            "background": (0, 0, 0),
            "red_team": (139, 0, 0),
            "green_team": (0, 100, 0),
            "text": (255, 255, 255),
            "input_box": (50, 50, 50),
            "active_box": (100, 100, 100)
        }
        
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        
        # Load logo
        try:
            self.original_logo = pygame.image.load("images/logo.jpg")
            self.logo = pygame.transform.scale(self.original_logo, (100, 100))
        except:
            self.original_logo = None
            self.logo = None
        
        self.splash_shown = False
        
        # Player entry data
        self.red_players = [{"id": "", "name": ""} for _ in range(15)]
        self.green_players = [{"id": "", "name": ""} for _ in range(15)]
        
        self.active_input = None # (team, index, field) where field is 'id' or 'name'
        
    def show_splash_screen(self):
        if not self.original_logo or self.splash_shown:
            return
            
        # Scale logo for splash screen
        splash_logo = pygame.transform.scale(self.original_logo, (871, 555))
        logo_rect = splash_logo.get_rect(center=(self.width // 2, self.height // 2))
        
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000: # 3 seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill(self.colors["background"])
            self.screen.blit(splash_logo, logo_rect)
            pygame.display.flip()
            clock.tick(60)
        
        self.splash_shown = True

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def run_player_entry(self):
        if not self.splash_shown:
            self.show_splash_screen()

        running = True
        while running:
            self.screen.fill(self.colors["background"])
            
            # Draw Title
            self.draw_text("PLAYER ENTRY", self.title_font, self.colors["text"], self.width//2 - 150, 20)
            
            if self.logo:
                self.screen.blit(self.logo, (10, 10))
            
            # Draw Column Headers
            self.draw_text("RED TEAM", self.font, self.colors["red_team"], 150, 80)
            self.draw_text("GREEN TEAM", self.font, self.colors["green_team"], 550, 80)
            
            # Draw Instructions
            self.draw_text("F5 - Start Game", self.font, self.colors["text"], self.width//2 - 150, 575)
            
            # Draw Input Boxes
            for i in range(15):
                # Red Team ID and Name
                y_pos = 120 + i * 30
                
                # Red ID
                color = self.colors["active_box"] if self.active_input == ("red", i, "id") else self.colors["input_box"]
                pygame.draw.rect(self.screen, color, (50, y_pos, 80, 25))
                self.draw_text(self.red_players[i]["id"], self.font, self.colors["text"], 55, y_pos)
                
                # Red Name
                color = self.colors["active_box"] if self.active_input == ("red", i, "name") else self.colors["input_box"]
                pygame.draw.rect(self.screen, color, (140, y_pos, 200, 25))
                self.draw_text(self.red_players[i]["name"], self.font, self.colors["text"], 145, y_pos)
                
                # Green ID
                color = self.colors["active_box"] if self.active_input == ("green", i, "id") else self.colors["input_box"]
                pygame.draw.rect(self.screen, color, (450, y_pos, 80, 25))
                self.draw_text(self.green_players[i]["id"], self.font, self.colors["text"], 455, y_pos)
                
                # Green Name
                color = self.colors["active_box"] if self.active_input == ("green", i, "name") else self.colors["input_box"]
                pygame.draw.rect(self.screen, color, (540, y_pos, 200, 25))
                self.draw_text(self.green_players[i]["name"], self.font, self.colors["text"], 545, y_pos)

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check which box was clicked
                    mouse_pos = pygame.mouse.get_pos()
                    self.active_input = None
                    for i in range(15):
                        # Red ID box
                        if pygame.Rect(50, 120 + i * 30, 80, 25).collidepoint(mouse_pos):
                            self.active_input = ("red", i, "id")
                        # Red Name box
                        elif pygame.Rect(140, 120 + i * 30, 200, 25).collidepoint(mouse_pos):
                            self.active_input = ("red", i, "name")
                        # Green ID box
                        elif pygame.Rect(450, 120 + i * 30, 80, 25).collidepoint(mouse_pos):
                            self.active_input = ("green", i, "id")
                        # Green Name box
                        elif pygame.Rect(540, 120 + i * 30, 200, 25).collidepoint(mouse_pos):
                            self.active_input = ("green", i, "name")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5: # Start game
                        running = False
                    
                    if self.active_input:
                        team, idx, field = self.active_input
                        player_list = self.red_players if team == "red" else self.green_players
                        
                        if event.key == pygame.K_BACKSPACE:
                            player_list[idx][field] = player_list[idx][field][:-1]
                        elif event.key == pygame.K_RETURN:
                            self.active_input = None
                        else:
                            if len(player_list[idx][field]) < 15:
                                player_list[idx][field] += event.unicode

        return self.red_players, self.green_players

if __name__ == "__main__":
    ui = PhotonUI()
    ui.run_player_entry()
