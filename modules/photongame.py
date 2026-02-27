from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer
from modules.ui import PhotonUI
from modules.player import Player
from modules.consolelog import log_game_event, log_game_tag_event
import time
from math import ceil

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, config:dict, server_host:str, server_ports):
        self.db = db
        self.server = PhotonServer(server_host, server_ports, self)
        self.ui = PhotonUI(self)

        # Game const vars
        self.POINTS_PLAYER_TAG = config["photon"]["game"]["points-player-tag"]
        self.POINTS_BASE_TAG = config["photon"]["game"]["points-base-tag"]
        self.GAME_LENGTH = config["photon"]["game"]["game-length"]

        # Game status vars
        self.start_game_flag = False
        self.game_in_progress:bool = False
        self.players = []
        self.game_events = []
        self.red_team_score = 0
        self.green_team_score = 0

        # Countdown vars
        self.COUNTDOWN_TIMER_LENGTH = (config["photon"]["game"]["start-countdown-length"] + 1) # This needs to be 1 second higher than the target timer length for format reasons
        self.countdown_active:bool = False
        self.countdown_time:float = -1.0 # This is the var to use in UI
        self.countdown_start_time:float = 0.0
    
    def update(self) -> bool:
        # Game update that runs each loop
        if self.start_game_flag:
            self.start_game()
        elif self.countdown_active:
            self.countdown_timer_update()
        elif self.game_in_progress:
            self.server.update()

        # Update UI
        window_open = self.ui.update()
        if not window_open:
            self.ui.kill_pygame()
            
        # Keep game running
        return window_open

    def countdown_timer_update(self):
        # Perform game start countdown timer operation
        time_elapsed = (time.time() - self.countdown_start_time)
        self.countdown_time = (self.COUNTDOWN_TIMER_LENGTH - time_elapsed)
        if ceil(self.countdown_time) == 1:
            self.countdown_active = False
            self.server.start_game()    # broadcast start signal to clients
            log_game_event("Countdown ended. LET IT RIP!")

    def start_game(self):
        # Starts the game.
        self.start_game_flag = False
        log_game_event("Game starting...")

        # Reset all players scores
        for player in self.players:
            player.score = 0

        # setup countdown timer
        self.countdown_time = self.COUNTDOWN_TIMER_LENGTH
        self.countdown_start_time = time.time()
        self.countdown_active = True
        log_game_event(f"Game beginning in {self.countdown_time - 1} seconds...")

        self.game_in_progress = True

    def end_game(self):
        # Ends the in progress game
        self.game_in_progress = False
        self.server.end_game()

    def clear_players(self):
        # Clears players from game
        self.players.clear()

    def add_new_player(self, pid: int, name: str, equipment_id: int, team: str) -> bool: 
        # Adds new player to the player list
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
        self.server.broadcast_message(str(equipment_id))
        # Function returns false anytime player is already in database
        return first_time_player

    def event_player_tag(self, tagger:Player, tagged:Player):
        # Handles event when player is tagged
        # Prevent sudoku
        if tagger.pid == tagged.pid:
            return

        # If players are enemies, tagger gets points.
        if tagger.team != tagged.team:
            tagger.score += self.POINTS_PLAYER_TAG

            # Update team score. For friendly fire, both players lose points.
            if tagger.team == 'Red':
                self.red_team_score += self.POINTS_PLAYER_TAG
            else:
                self.green_team_score += self.POINTS_PLAYER_TAG

            log_game_event(f"{tagger.name} >>> {tagged.name}")
            self.game_events.append(f"{tagger.name} tagged {tagged.name}")
            self.server.broadcast_tagged(tagged.equipment_id)
        else:
            tagger.score -= self.POINTS_PLAYER_TAG
            tagged.score -= self.POINTS_PLAYER_TAG

            if tagger.team == 'Red':
                self.red_team_score -= self.POINTS_PLAYER_TAG
            else:
                self.green_team_score -= self.POINTS_PLAYER_TAG

            log_game_event(f"{tagger.name} >>> {tagged.name}")
            self.game_events.append(f"{tagger.name} friendly fired on {tagged.name}")
            self.server.broadcast_tagged(tagged.equipment_id)
            self.server.broadcast_tagged(tagger.equipment_id)
    
    def event_base_tag(self, tagger:Player, base_code:int):
        if tagger.team == "Red" and base_code == server.GREEN_BASE_HIT:
            tagger.score += self.POINTS_BASE_TAG
            log_game_event(f"{tagger.name} >>> Green Base")
            self.game_events.append(f"{tagger.name} tagged Green Base")
        elif tagger.team == "Green" and base_code == server.RED_BASE_HIT:
            tagger.score += self.POINTS_BASE_TAG
            log_game_event(f"{tagger.name} >>> Red Base")
            self.game_events.append(f"{tagger.name} tagged Red Base")