import os

class FileUtils:
    @staticmethod
    def save_transcript(text, filename="transcript.txt"):
        with open(filename, "w") as file:
            file.write(text)
        print(f"Transcript saved to {filename}")

    @staticmethod
    def read_transcript(filename="transcript.txt"):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return file.read()
        return None
