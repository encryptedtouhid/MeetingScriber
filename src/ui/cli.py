from services.audio_capture import AudioCapture
from services.transcriber import Transcriber
from utils.file_utils import FileUtils

def run_cli():
    capture = AudioCapture()
    transcriber = Transcriber()

    print("Starting recording...")
    audio_data = capture.start_recording(duration=10)  # Adjust duration

    print("Transcribing...")
    transcript = transcriber.transcribe_audio(audio_data)

    print("\n--- Transcription ---")
    print(transcript)

    FileUtils.save_transcript(transcript)

if __name__ == "__main__":
    run_cli()
