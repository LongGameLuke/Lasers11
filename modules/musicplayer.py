import pygame
import random
from modules.consolelog import log_process

class MusicPlayer:
    def __init__(self, track_list:list):
        pygame.mixer.init()
        self.track_list:list = track_list
        self.loaded_track = None
        self.volume:float = 1.0
    
    def load_track_random(self):
        # Loads random audio track from track_list into loaded_track
        track_count = len(self.track_list)
        track_int = random.randint(0, (track_count - 1))
        self.loaded_track = self.track_list[track_int]
        pygame.mixer.music.load(self.loaded_track)

    def play(self):
        # Plays currently loaded audio file

        # Checks to make sure audio is not playing
        # and audio is loaded
        if self.loaded_track == None:
            log_process("MusicPlayer: No song to play. No song loaded.")
            return

        pygame.mixer.music.play()

    def stop(self):
        # Stops currently playing audio
        if self.is_playing() == False:
            log_process("MusicPlayer: No music is currently playing")
            return

        pygame.mixer.music.stop()

    def is_playing(self)->bool:
        # Returns if music is currently playing
        return pygame.mixer.music.get_busy()