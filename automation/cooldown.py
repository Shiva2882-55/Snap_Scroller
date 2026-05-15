import time

class Cooldown:
    def __init__(self, seconds):
        self.seconds = seconds
        self.last_time = 0

    def ready(self):
        return (time.time() - self.last_time) >= self.seconds

    def trigger(self):
        self.last_time = time.time()
