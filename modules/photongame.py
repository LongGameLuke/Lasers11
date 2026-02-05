from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer
from modules.photonui import PhotonUI
from time import sleep

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, server:PhotonServer):
        self.db = db
        self.server = server
        self.ui = PhotonUI()
        
        # Start player entry screen
        self.red_players, self.green_players = self.ui.run_player_entry()
    
    def update(self) -> bool:
        self.server.update()
        sleep(1)

        # Keep game running
        return True
