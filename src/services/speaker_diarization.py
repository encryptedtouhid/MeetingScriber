from pyannote.audio.pipelines.speaker_diarization import SpeakerDiarization
from pyannote.core import Segment

class SpeakerDiarizationService:
    def __init__(self, model_path="pyannote/speaker-diarization"):
        self.pipeline = SpeakerDiarization.from_pretrained(model_path)

    def diarize(self, audio_file):
        diarization = self.pipeline(audio_file)
        speaker_segments = []

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append(f"{speaker}: {turn.start:.1f}s --> {turn.end:.1f}s")

        return speaker_segments
