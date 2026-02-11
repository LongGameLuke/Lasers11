from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer
from modules.photonui import PhotonUI
from modules.player import Player
from time import sleep

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, server:PhotonServer):
        self.db = db
        self.server = server
        self.ui = PhotonUI(self)
        
        # Run UI
        self.ui.run()
    
    def update(self) -> bool:
        self.server.update()
        sleep(1)

        # Keep game running
        return True

    def start_game(self):
        # Starts the game when called
        self.server.start_game()

    def clear_players(self):
        self.server.players.clear()

    def add_new_player(self, pid: int, name: str, equipment_id: int, team: str) -> bool: 
        for p in self.server.players:
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
        self.server.players.append(new_player)
        self.server.broadcast_message(str(equipment_id))
        # Function returns false anytime player is already in database
        return first_time_player