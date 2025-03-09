import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
from services.audio_capture import AudioCapture
from services.transcriber import Transcriber
from utils.file_utils import FileUtils

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meeting Scriber")
        self.root.geometry("600x400")

        # Title Label
        self.label = tk.Label(root, text="Meeting Scriber", font=("Arial", 16))
        self.label.pack(pady=10)

        # Transcription Text Box
        self.text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
        self.text_box.pack(padx=10, pady=10)

        # Start Button
        self.start_btn = tk.Button(root, text="Start Transcription", command=self.start_transcription)
        self.start_btn.pack(pady=5)

        # Save Button
        self.save_btn = tk.Button(root, text="Save Transcription", command=self.save_transcription)
        self.save_btn.pack(pady=5)

        self.audio_capture = AudioCapture()
        self.transcriber = Transcriber()

    def start_transcription(self):
        """Runs transcription in a separate thread."""
        self.text_box.delete("1.0", tk.END)  # Clear previous transcription
        self.text_box.insert(tk.END, "Recording and transcribing...\n")
        thread = Thread(target=self.record_and_transcribe)
        thread.start()

    def record_and_transcribe(self):
        """Captures audio and updates transcription in real-time."""
        audio_data = self.audio_capture.start_recording(duration=10)  # Adjust as needed
        transcript = self.transcriber.transcribe_audio(audio_data)

        self.text_box.delete("1.0", tk.END)  # Clear previous transcription
        self.text_box.insert(tk.END, transcript)

    def save_transcription(self):
        """Saves transcription to a file."""
        text = self.text_box.get("1.0", tk.END).strip()
        if text:
            FileUtils.save_transcript(text)
            self.text_box.insert(tk.END, "\n\nTranscript saved successfully!")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
