from time import time

class Timer:
    def __init__(self, length):
        self.length = float(length)
        self.active:bool = False
        self.start_time:float = -1.0
        self.time:float = -1.0
        self.completed:bool = False

    def start(self):
        self.active = True
        self.start_time = time()
        print(f"Timer start: {self.length} seconds")

    def update(self):
        if self.active:
            time_elapsed = (time() - self.start_time)
            self.time = (self.length - time_elapsed)
            if self.time <= 0.0:
                self.active = False
                self.completed = True

    def reset(self):
        self.active = False
        self.start_time = -1.0
        self.time = -1.0
        self.completed = False