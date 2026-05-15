import time

class ImpulseFilter:
    """
    Filters out long-duration sounds (speech, music).
    Designed for repeated short impulses like snaps.
    """

    def __init__(self, max_duration_ms=120):
        self.max_duration = max_duration_ms / 1000.0
        self.start_time = None
        self.active = False

    def update(self, rms, threshold):
        now = time.time()

        # Start of a sound
        if rms > threshold and not self.active:
            self.start_time = now
            self.active = True
            return True  # allow start of impulse

        # Sound continues
        if rms > threshold and self.active:
            # If sound is too long → reject
            if (now - self.start_time) > self.max_duration:
                self.reset()
                return False
            return True

        # Sound ended → reset state
        if rms <= threshold and self.active:
            self.reset()
            return True

        return False

    def reset(self):
        self.start_time = None
        self.active = False
