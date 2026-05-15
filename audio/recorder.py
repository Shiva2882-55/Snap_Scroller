import sounddevice as sd
from config.settings import SAMPLE_RATE, CHUNK_SIZE

class AudioRecorder:
    def __init__(self):
        self.stream = None

    def start(self, callback):
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=CHUNK_SIZE,
            callback=self._callback(callback)
        )
        self.stream.start()

    def _callback(self, user_callback):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            audio = indata[:, 0].copy()
            user_callback(audio)
        return callback

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
