import numpy as np

class AudioProcessor:
    @staticmethod
    def rms(audio):
        """Root Mean Square energy"""
        return np.sqrt(np.mean(audio ** 2))

    @staticmethod
    def zero_crossing_rate(audio):
        """Zero Crossing Rate (not used now, but kept)"""
        return np.mean(np.abs(np.diff(np.sign(audio)))) / 2

    @staticmethod
    def band_energy(audio, sample_rate=44100):
        """
        Splits signal energy into:
        - Low Frequency (< 2 kHz) → voice / music
        - High Frequency (> 2 kHz) → snaps
        """
        # FFT
        fft = np.fft.rfft(audio)
        freqs = np.fft.rfftfreq(len(audio), d=1 / sample_rate)

        mag = np.abs(fft)

        # Frequency bands
        low_band = mag[freqs < 2000]
        high_band = mag[freqs >= 2000]

        lf_energy = np.sum(low_band)
        hf_energy = np.sum(high_band)

        return lf_energy, hf_energy
