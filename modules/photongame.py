from modules.photondb import PhotonDB
from modules.photonserver import PhotonServer, SERVER_CODES
from modules.ui import PhotonUI
from modules.player import Player
from modules.consolelog import log_game_event, log_game_tag_event
from modules.timer import Timer
from modules.musicplayer import MusicPlayer
import time

class PhotonGame:
    # This class runs the actual game after initialization
    def __init__(self, db:PhotonDB, config:dict, server_host:str, server_ports):
        self.db = db
        self.config = config
        self.server = PhotonServer(server_host, server_ports, self)
        self.ui = PhotonUI(self)

        # Game const vars
        self.POINTS_PLAYER_TAG = config["photon"]["game"]["points-player-tag"]
        self.POINTS_BASE_TAG = config["photon"]["game"]["points-base-tag"]
        self.COUNTDOWN_LENGTH = config["photon"]["game"]["start-countdown-length"]
        self.GAME_LENGTH = config["photon"]["game"]["game-length"]

        # Game status vars
        self.start_game_flag = False
        self.game_in_progress:bool = False
        self.players = []
        self.game_events = []
        self.timer = Timer(self.COUNTDOWN_LENGTH) # Used for countdown and game time
        self.music = MusicPlayer(config["photon"]["game"]["music"]["tracks"])
    
    def update(self) -> bool:
        # Game update that runs each loop
        # Update timer
        if self.timer.completed == True and self.game_in_progress == False:
            # Start game timer
            self.game_in_progress = True
            self.timer.reset()
            self.timer.length = float(self.GAME_LENGTH)
            self.timer.start()
            log_game_event("Countdown ended. LET IT RIP!")
            self.server.start_game() # Tell server to broadcast start signal
        elif self.timer.completed == True and self.game_in_progress == True:
            # Reset timer and end game
            self.end_game()
            self.timer.reset()
            self.timer.length = float(self.COUNTDOWN_LENGTH)
        self.timer.update()

        if self.start_game_flag:
            self.start_game()
        elif self.game_in_progress:
            self.server.update()

        # Update UI
        window_open = self.ui.update()
        if not window_open:
            self.ui.kill_pygame()
            
        # Keep game running
        return window_open

    def start_game(self):
        # Starts the game.
        self.start_game_flag = False
        log_game_event("Game starting...")

        # Reset players to default state
        self.reset_game()

        # setup countdown timer
        self.timer.start()
        log_game_event(f"Game beginning in {self.COUNTDOWN_LENGTH} seconds...")

        # Start music track
        self.music.load_track_random()
        self.music.play()

    def end_game(self, kill_music=False):
        # Ends the in progress game
        self.game_in_progress = False
        self.server.end_game()
        
        if kill_music:
            self.music.stop()
    
    def reset_game(self):
        # Sets all players scores to zero and clears events
        for player in self.players:
            player.reset_score()
        self.game_events = []
        self.timer.reset()
        self.timer.length = float(self.COUNTDOWN_LENGTH)

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

            log_game_event(f"{tagger.name} >>> {tagged.name}")
            self.game_events.append(f"{tagger.name} tagged {tagged.name}")
            self.server.broadcast_tagged(tagged.equipment_id)
        else:
            tagger.score -= self.POINTS_PLAYER_TAG
            tagged.score -= self.POINTS_PLAYER_TAG

            log_game_event(f"{tagger.name} >>> {tagged.name}")
            self.game_events.append(f"{tagger.name} friendly fired on {tagged.name}")
            self.server.broadcast_tagged(tagged.equipment_id)
            self.server.broadcast_tagged(tagger.equipment_id)

    def get_team_score(self, team: str) -> int:
        # Returns current team score
        team_score = 0
        for player in self.players:
            if player.team == team:
                team_score += player.score
        return team_score
    
    def is_team_winning(self, team: str) -> bool:
        if team == 'Red':
            return self.get_team_score('Red') > self.get_team_score('Green')
        else:
            return self.get_team_score('Green') > self.get_team_score('Red')

    def event_base_tag(self, tagger:Player, base_code:int):
        # Handles base tag event
        if tagger.team == "Red" and base_code == int(SERVER_CODES.GREEN_BASE_HIT.value):
            tagger.score += self.POINTS_BASE_TAG
            tagger.base_tag = True
            log_game_event(f"{tagger.name} >>> Green Base")
            self.game_events.append(f"{tagger.name} tagged Green Base")
            self.server.broadcast_tagged(int(SERVER_CODES.GREEN_BASE_HIT.value))
        elif tagger.team == "Green" and base_code == int(SERVER_CODES.RED_BASE_HIT.value):
            tagger.score += self.POINTS_BASE_TAG
            tagger.base_tag = True
            log_game_event(f"{tagger.name} >>> Red Base")
            self.game_events.append(f"{tagger.name} tagged Red Base")
            self.server.broadcast_tagged(int(SERVER_CODES.RED_BASE_HIT.value))