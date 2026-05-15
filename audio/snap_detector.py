import time


class SnapDetector:
    """
    Detects snap-like sounds using calibrated audio thresholds.
    Thresholds MUST be provided dynamically (from calibration).
    """

    def __init__(
        self,
        rms_min: float,
        peak_min: float,
        hf_ratio_min: float,
        min_interval: float = 0.5
    ):
        # Dynamic thresholds (from calibration)
        self.RMS_MIN = rms_min
        self.PEAK_MIN = peak_min
        self.HF_RATIO_MIN = hf_ratio_min

        # Cooldown (seconds)
        self.min_interval = min_interval
        self.last_trigger_time = 0.0

    def _cooldown_active(self) -> bool:
        return (time.time() - self.last_trigger_time) < self.min_interval

    def detect(self, rms: float, peak: float, hf_ratio: float) -> bool:
        """
        Returns True if a snap is detected, otherwise False.
        """

        # Cooldown check
        if self._cooldown_active():
            return False

        # Threshold checks
        if rms < self.RMS_MIN:
            return False

        if peak < self.PEAK_MIN:
            return False

        if hf_ratio < self.HF_RATIO_MIN:
            return False

        # Snap detected
        self.last_trigger_time = time.time()
        return True

    def debug_state(self) -> dict:
        """
        Useful for debugging and logging.
        """
        return {
            "RMS_MIN": self.RMS_MIN,
            "PEAK_MIN": self.PEAK_MIN,
            "HF_RATIO_MIN": self.HF_RATIO_MIN,
            "cooldown_active": self._cooldown_active()
        }
