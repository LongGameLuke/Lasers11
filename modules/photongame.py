from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer
from time import sleep

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, server:PhotonServer):
        self.db = db
        self.server = server
    
    def update(self) -> bool:
        self.server.update()
        sleep(1)

        # Keep game running
        return True
