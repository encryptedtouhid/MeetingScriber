import sounddevice as sd
import numpy as np
import queue

class AudioCapture:
    def __init__(self, sample_rate=44100, channels=1, device=None):
        self.sample_rate = sample_rate
        self.channels = channels
        self.q = queue.Queue()
        self.device = self.get_loopback_device() if device is None else device

    def get_loopback_device(self):
        """Automatically find a suitable loopback device."""
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if "loopback" in dev["name"].lower() or "stereo mix" in dev["name"].lower():
                return i
        raise ValueError("No loopback or stereo mix device found. Enable 'Stereo Mix' in sound settings.")

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def start_recording(self, duration=10):
        if self.device is None:
            raise ValueError("No valid loopback device found.")

        with sd.InputStream(callback=self._callback, channels=self.channels, samplerate=self.sample_rate, device=self.device):
            print(f"Recording started using device {self.device}...")
            sd.sleep(duration * 1000)
            print("Recording finished.")

        return np.concatenate(list(self.q.queue), axis=0)

