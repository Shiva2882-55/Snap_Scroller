import time
import numpy as np
import sounddevice as sd

from audio.snap_detector import SnapDetector
from audio.snap_trainer import SnapTrainer
from automation.scroller import Scroller

# from core.snap_gate import SnapGate
from core.impulse_filter import ImpulseFilter


# ==============================
# CONFIG
# ==============================
SAMPLE_RATE = 44100
BLOCK_SIZE = 2048


# ==============================
# FEATURE EXTRACTION
# ==============================
def extract_features(audio, samplerate):
    audio = audio[:, 0]  # mono

    rms = np.sqrt(np.mean(audio ** 2))
    peak = np.max(np.abs(audio))

    fft = np.abs(np.fft.rfft(audio))
    freqs = np.fft.rfftfreq(len(audio), 1 / samplerate)

    hf_energy = np.sum(fft[freqs > 2000])
    total_energy = np.sum(fft) + 1e-9
    hf_ratio = min(hf_energy / total_energy, 1.0)

    return rms, peak, hf_ratio

# ==============================
# SNAP TRAINING STATE
# ==============================
trainer = SnapTrainer(required_snaps=5)
training_done = False
detector = None

# ==============================
# SCROLLING + SMART FILTERS
# ==============================
scroller = Scroller(scroll_amount=-500)

# snap_gate = SnapGate(window_sec=3.0)          # double snap within 3 sec
impulse_filter = ImpulseFilter(max_duration_ms=200)  # block speech

snap_active = False # for rising edge detection

print("\n🫰 SNAP TRAINING MODE")
print("Please snap your fingers 5 times clearly...\n")

# ==============================
# AUDIO CALLBACK
# ==============================
def audio_callback(indata, frames, time_info, status):
    global training_done, detector

    if status:
        return

    rms, peak, hf_ratio = extract_features(indata, SAMPLE_RATE)

    # -------- TRAINING PHASE --------
    if not training_done:
        if rms > 0.002 and peak > 0.02:
            trainer.add_sample(rms, peak, hf_ratio)
            print(f"✔ Snap captured ({len(trainer.snap_features)}/5)")

        if trainer.is_complete():
            thresholds = trainer.get_thresholds()

            detector = SnapDetector(
                rms_min=thresholds["RMS_MIN"],
                peak_min=thresholds["PEAK_MIN"],
                hf_ratio_min=thresholds["HF_RATIO_MIN"],
                min_interval=0.7
            )

            training_done = True
            print("\n✅ Snap training complete!")
            print("🎬 You can now scroll videos using snaps!\n")

        return

    # -------- DETECTION PHASE --------
    global snap_active

    if detector.detect(rms, peak, hf_ratio):

        # Reject long sounds (speech, reels)
        # Allow snap detector to decide; impulse filter only blocks obvious speech
        if not impulse_filter.update(rms, detector.RMS_MIN):
            snap_active = False
            return


         # ⭐ RISING EDGE DETECTION
        if not snap_active:
            snap_active = True
            print("🖱️ SCROLL (single snap)")
            scroller.scroll()

        else:
            # Sound ended → ready for next snap
            snap_active = False



# ==============================
# MAIN LOOP
# ==============================
print("🎧 Listening... Press Ctrl+C to stop")

try:
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=1,
        callback=audio_callback
    ):
        while True:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Program stopped")

