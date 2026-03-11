from time import time

class Timer:
    def __init__(self, length):
        self.length:float = float(length)
        self.active:bool = False
        self.start_time:float = -1.0
        self.time:float = -1.0
        self.completed:bool = False
    
    def __str__(self):
        # return formatted string of remaining time
        total_seconds = int(max(0, self.time))
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start(self):
        # start timer
        self.active = True
        self.start_time = time()

    def update(self):
        # general update to refresh timer
        if self.active:
            time_elapsed = (time() - self.start_time)
            self.time = (self.length - time_elapsed)
            if self.time <= 0.0:
                self.active = False
                self.completed = True

    def reset(self):
        # reset timer back to default values
        self.active = False
        self.start_time = -1.0
        self.time = -1.0
        self.completed = False