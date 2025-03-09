import whisper
import numpy as np

class Transcriber:
    def __init__(self, model_type="base"):
        self.model = whisper.load_model(model_type)

    def transcribe_audio(self, audio_data, sample_rate=44100):
        audio_data = np.int16(audio_data * 32767)  # Normalize audio
        result = self.model.transcribe(audio_data)
        return result["text"]
