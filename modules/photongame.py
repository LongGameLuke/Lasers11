from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, server:PhotonServer):
        self.db = db
        self.server = server
    
    def update(self):
        self.server.update()
