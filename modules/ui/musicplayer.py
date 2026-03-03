import pygame
import random

class MusicPlayer:
    def __init__(self, track_list):
        pygame.mixer.init()
        self.track_list = track_list
        self.loaded_song = None

    def load_track(self, track_index:int):
        pass
    
    def load_track_random(self):
        # Loads random audio track from track_list into loaded_song
        track_count = len(self.track_list)
        track_int = random.randint(0, track_count)
        self.loaded_song = self.track_list[track_int]
        pygame.mixer.music.load(self.loaded_song)

    def play(self):
        # Plays currently loaded audio file

        # Return if no song has been loaded
        if self.loaded_song == None:
            print("No song to play. No song loaded.")
            return
        
        pygame.music.mixer.play()

    def stop(self):
        # Stops currently playing audio
        if self.isPlaying == False:
            print("No music is currently playing")
            return
        
        pygame.music.mixer.stop()

    def is_playing(self)->bool:
        return pygame.music.mixer.get_busy()