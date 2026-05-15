import numpy as np
from audio.snap_detector import SnapDetector

def test_snap():
    detector = SnapDetector()

    fake_snap = np.random.uniform(-1, 1, 1024)
    detected = detector.detect(fake_snap)

    print("Snap detected:", detected)

if __name__ == "__main__":
    test_snap()
