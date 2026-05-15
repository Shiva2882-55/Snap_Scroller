import numpy as np
import time

class SnapTrainer:
    """
    Trains snap detection thresholds using real user snaps.
    """

    def __init__(self, required_snaps=5):
        self.required_snaps = required_snaps
        self.snap_features = []

    def add_sample(self, rms, peak, hf_ratio):
        self.snap_features.append((rms, peak, hf_ratio))

    def is_complete(self):
        return len(self.snap_features) >= self.required_snaps

    def get_thresholds(self):
        rms_vals = [x[0] for x in self.snap_features]
        peak_vals = [x[1] for x in self.snap_features]
        hf_vals = [x[2] for x in self.snap_features]

        # Use median for robustness
        rms_base = np.median(rms_vals)
        peak_base = np.median(peak_vals)
        hf_base = np.median(hf_vals)

        return {
            "RMS_MIN": rms_base * 0.6,      # snaps must exceed most snap energy
            "PEAK_MIN": peak_base * 0.6,
            "HF_RATIO_MIN": max(hf_base * 0.7, 0.18)
        }
