class Player:
    def __init__(self):
        # player identity info
        self.pid:int = -1
        self.name:str = ""
        self.equipment_id:int = -1

        # game status info
        self.team:str = ""
        self.score:int = 0
        self.base_tag:bool = False

    def __str__(self):
        return f"PID: {self.pid}\nName: {self.name}\nEquipment ID: {self.equipment_id}\n\nTeam: {self.team}\nScore: {self.score}"