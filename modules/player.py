from modules.photonserver import TEAMS

class Player:
    def __init__(self):
        self.pid:int = -1
        self.name:str = ""
        self.equipment_id:int = -1
        self.team:TEAMS = NONE