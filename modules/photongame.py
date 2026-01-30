from modules.photondb import PhotonDB

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, ports:dict):
        self.db = db
        self.ports = ports
    
    def update(self):
        pass
