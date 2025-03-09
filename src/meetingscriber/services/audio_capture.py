import sounddevice as sd
import numpy as np
import queue

class AudioCapture:
    def __init__(self, sample_rate=44100, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.q = queue.Queue()

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def start_recording(self, duration=10):
        with sd.InputStream(callback=self._callback, channels=self.channels, samplerate=self.sample_rate, device="loopback"):
            print("Recording started...")
            sd.sleep(duration * 1000)
            print("Recording finished.")

        return np.concatenate(list(self.q.queue), axis=0)
