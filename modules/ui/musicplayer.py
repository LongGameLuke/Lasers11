import pygame
import random

class MusicPlayer:
    def __init__(self, track_list:list):
        pygame.mixer.init()
        self.track_list:list = track_list
        self.loaded_song = None
        self.volume:float = 1.0
    
    def load_track_random(self):
        # Loads random audio track from track_list into loaded_song
        track_count = len(self.track_list)
        track_int = random.randint(0, track_count)
        self.loaded_song = self.track_list[track_int]
        pygame.mixer.music.load(self.loaded_song)

    def play(self):
        # Plays currently loaded audio file

        # Checks to make sure audio is not playing
        # and audio is loaded
        if self.loaded_song == None:
            print("No song to play. No song loaded.")
            return
        elif self.is_playing():
            print("Song is already playing.")
            return
        
        pygame.music.mixer.play()

    def stop(self):
        # Stops currently playing audio
        if self.is_playing() == False:
            print("No music is currently playing")
            return
        
        pygame.music.mixer.stop()

    def is_playing(self)->bool:
        # Returns if music is currently playing
        return pygame.music.mixer.get_busy()