import numpy as np

class AudioCalibrator:
    """
    Calibrates ambient audio noise and produces
    safe, realistic snap detection thresholds.
    """

    def __init__(self):
        self.rms_values = []
        self.peak_values = []
        self.hf_ratios = []

    def process_chunk(self, audio_chunk, samplerate):
        """
        Processes a single audio chunk during calibration.
        """

        # --- Convert to mono (SAFE) ---
        audio = audio_chunk[:, 0]

        # --- RMS energy ---
        rms = np.sqrt(np.mean(audio ** 2))

        # --- Peak amplitude ---
        peak = np.max(np.abs(audio))

        # --- FFT for frequency analysis ---
        fft = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), 1 / samplerate)

        # --- High-frequency energy (>2kHz) ---
        hf_energy = np.sum(fft[freqs > 2000])
        total_energy = np.sum(fft) + 1e-9

        # ==================================================
        # 🔧 FIX #1 (CRITICAL BUG FIX)
        # HF ratio MUST be between 0 and 1
        # Earlier it could exceed 1 → impossible threshold
        # ==================================================
        hf_ratio = min(hf_energy / total_energy, 1.0)

        # Store values
        self.rms_values.append(rms)
        self.peak_values.append(peak)
        self.hf_ratios.append(hf_ratio)

    def get_thresholds(self):
        rms_base = np.mean(self.rms_values)
        peak_base = np.mean(self.peak_values)
        hf_base = np.mean(self.hf_ratios)

        return {
            "RMS_MIN": rms_base * 2.5,          # ↓ relaxed
            "PEAK_MIN": peak_base * 3.0,        # ↓ relaxed
            "HF_RATIO_MIN": min(
             max(hf_base * 0.6, 0.18),       # floor
             0.45                            # hard cap
        )
    }

