from modules.photonserver import TEAMS

class Player:
    def __init__(self):
        # player identity info
        self.pid:int = -1
        self.name:str = ""
        self.equipment_id:int = -1

        # game status info
        self.team = ""
        self.score = 0