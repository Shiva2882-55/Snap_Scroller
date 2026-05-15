import sounddevice as sd

def check_microphone():
    try:
        sd.query_devices(kind="input")
        return True
    except Exception:
        return False
