from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer
from modules.photonui import PhotonUI
from modules.player import Player
import time
from math import ceil

POINTS_PER_TAG = 50
POINTS_PER_BASE_TAG = 150

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, server_host:str, server_ports):
        self.db = db
        self.server = PhotonServer(server_host, server_ports, self)
        self.ui = PhotonUI(self)

        # Game vars
        self.start_game_flag = False
        self.game_in_progress:bool = False
        self.players = []

        # Countdown vars
        self.countdown_active:bool = False
        self.countdown_time:float = -1.0 # This is the var to use in UI
        self.countdown_timer_length = 6
        self.start_time:float = 0.0
    
    def update(self) -> bool:
        if self.start_game_flag:
            self.start_game_flag = False
            self.start_game()
        elif self.countdown_active:
            self.countdown_timer_update()
        elif self.game_in_progress:
            self.server.update()

        # Update UI
        window_still_open = self.ui.update()
        if not window_still_open:
            self.ui.kill_pygame()

        # Keep game running
        return window_still_open

    def countdown_timer_update(self):
        time_elapsed = (time.time() - self.start_time)
        self.countdown_time = (self.countdown_timer_length - time_elapsed)
        if ceil(self.countdown_time) == 0:
            self.countdown_active = False

    def start_game(self):
        # Starts the game.
        # Reset all players scores
        for player in self.players:
            player.score = 0

        # setup countdown timer
        self.countdown_time = 6 # This needs to be 6 to count down for a full 5 seconds
        self.start_time = time.time()
        self.countdown_active = True

        self.game_in_progress = True
        self.server.start_game()

    def end_game(self):
        # Ends the in progress game
        self.game_in_progress = False
        self.server.end_game()

    def clear_players(self):
        # Clears players from game
        self.players.clear()

    def add_new_player(self, pid: int, name: str, equipment_id: int, team: str) -> bool: 
        for p in self.players:
            if p.pid == pid:
                raise ValueError(f"Player is already in game!")
        
        first_time_player:bool = self.db.add_player(pid, name)
        if not first_time_player:
            existing = self.db.get_player_by_pid(pid)
            if existing and existing[1] != name:
                raise ValueError(f"PID unavailable, taken by player: {existing[1]}")
        
        new_player = Player()
        new_player.pid = pid
        new_player.name = name
        new_player.equipment_id = equipment_id
        new_player.team = team
        self.players.append(new_player)
        # Function returns false anytime player is already in database
        return first_time_player
    
    def event_player_tag(self, tagger:Player, tagged:Player):
        # Handles event when player is tagged

        # Prevent sudoku
        if tagger == tagger:
            return

        # Ensure players are on opposing teams
        # 
        if tagger.team != tagged.team:
            tagger.score += POINTS_PER_TAG
            self.server.broadcast_tagged(tagged.equipment_id)
