import pygame
import random
from modules.consolelog import log_process

class MusicPlayer:
    def __init__(self, track_list:list):
        pygame.mixer.init()
        self.track_list:list = track_list
        self.loaded_track = None
        self.volume:float = 1.0
        self.is_playing = False
    
    def load_track_random(self) -> bool:
        # Loads random audio track from track_list into loaded_track
        if self.is_playing:
            # stop audio before loading new track
            self.stop()

        track_count = len(self.track_list)
        track_int = random.randint(0, (track_count - 1))
        self.loaded_track = self.track_list[track_int]
        try:
            pygame.mixer.music.load(self.loaded_track)
            return True
        except Exception as e:
            raise e

    def play(self):
        # Plays currently loaded audio file

        # Checks to make sure audio is not playing
        # and audio is loaded
        if self.loaded_track == None:
            log_process("MusicPlayer: No song to play. No song loaded.")
            return
        elif self.is_playing:
            log_process("MusicPlayer: Music already playing.")
            return

        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        # Stops currently playing audio
        if self.is_playing() == False:
            log_process("MusicPlayer: No music is currently playing")
            return

        pygame.mixer.music.stop()
        self.is_playing = False