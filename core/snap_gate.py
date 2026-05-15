import time

class SnapGate:
    """
    Allows scrolling only if snaps occur
    within a given time window.
    """

    def __init__(self, window_sec=3.0):
        self.window_sec = window_sec
        self.last_snap_time = None

    def allow(self):
        now = time.time()

        if self.last_snap_time is None:
            self.last_snap_time = now
            return False  # first snap → wait

        if now - self.last_snap_time <= self.window_sec:
            self.last_snap_time = None
            return True   # second snap within window

        # too late → reset
        self.last_snap_time = now
        return False
