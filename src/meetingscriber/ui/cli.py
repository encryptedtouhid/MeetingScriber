from src.meetingscriber.services.audio_capture import AudioCapture
from src.meetingscriber.services.transcriber import Transcriber
from src.meetingscriber.utils.file_utils import FileUtils

def run_cli():
    try:
        capture = AudioCapture()
        transcriber = Transcriber()

        print("Starting recording...")
        audio_data = capture.start_recording(duration=10)
        print("Captured audio shape:", audio_data.shape)

        print("Transcribing...")
        transcript = transcriber.transcribe_audio(audio_data)

        print("\n--- Transcription ---")
        print(transcript)
        FileUtils.save_transcript(transcript)

    except ValueError as e:
        print("Error:", e)
if __name__ == "__main__":
    run_cli()
