# =========================
# AUDIO CONFIG
# =========================

SAMPLE_RATE = 44100        # Standard mic sample rate
CHUNK_SIZE = 2048          # ~46 ms per chunk (good for snaps)

# =========================
# SNAP DETECTION THRESHOLDS
# =========================

# RMS & peak (calibrated from YOUR logs)
RMS_MIN = 0.00015          # allows weak snaps
PEAK_MIN = 0.0015          # blocks video sound & voice

# Frequency-based filtering
HF_RATIO_MIN = 0.02        # snap has more high-frequency energy

# Snap duration window (ms)
MIN_SNAP_MS = 20
MAX_SNAP_MS = 120

# Cooldown to prevent multi-skip
COOLDOWN_SECONDS = 3.0     # your requested delay
