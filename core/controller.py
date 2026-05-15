# core/controller.py

import time
from audio.snap_detector import SnapDetector
from automation.scroller import scroll_next
from config.settings import COOLDOWN_SECONDS


class SnapController:
    def __init__(self):
        self.detector = SnapDetector()
        self.last_trigger_time = 0

    def process_audio(self, audio_chunk):
        """
        Called continuously by the audio recorder.
        Decides whether a snap happened and triggers action.
        """
        now = time.time()

        if self.detector.detect(audio_chunk):
            if now - self.last_trigger_time >= COOLDOWN_SECONDS:
                print("👆 SNAP DETECTED → NEXT REEL")
                scroll_next()
                self.last_trigger_time = now
