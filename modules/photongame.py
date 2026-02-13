from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer
from modules.photonui import PhotonUI
from modules.player import Player
from time import sleep

POINTS_PER_TAG = 50
POINTS_PER_BASE_TAG = 150

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, server:PhotonServer):
        self.db = db
        self.server = server
        self.ui = PhotonUI(self)

        # Game vars
        self.game_in_progress:bool = False
        self.players:list = []
        
        # Run UI
        self.ui.run()
    
    def update(self) -> bool:
        self.server.update()

        # Keep game running
        return True

    def start_game(self):
        # Starts the game
        self.server.start_game()

    def clear_players(self):
        # Clears players from game
        self.server.players.clear()

    def add_new_player(self, pid: int, name: str, equipment_id: int, team: str) -> bool: 
        for p in self.players:
            if p.pid == pid:
                raise ValueError(f"Player is already in game!")
        
        first_time_player = self.db.add_player(pid, name)
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
        self.server.broadcast_message(str(equipment_id))
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
