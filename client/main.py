import asyncio
import json
import os
import sys
from typing import Dict

import websockets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Client configuration
SERVER_URL = os.getenv('SERVER_URL', 'ws://localhost:8000/transcribe')

class TranscriptionClient:
    def __init__(self):
        self.active_speakers: Dict[str, bool] = {}

    def print_transcription(self, client_id: str, text: str, is_final: bool):
        # Clear line and move cursor up if needed
        if not is_final:
            sys.stdout.write("\033[K")  # Clear line
            sys.stdout.write("\033[F" * (len(self.active_speakers) - 1))  # Move cursor up
        
        # Format and print the transcription
        prefix = "[FINAL]" if is_final else "[interim]"
        speaker_line = f"Speaker {client_id[:8]}: {prefix} {text}"
        print(speaker_line)

        if not is_final:
            # Move cursor back down
            sys.stdout.write("\n" * (len(self.active_speakers) - 1))

    async def connect(self):
        print("\n" * len(self.active_speakers))  # Initial newlines for transcription space
        print("Connected to transcription server. Waiting for speakers...")
        print("Press Ctrl+C to exit")

        while True:
            try:
                async with websockets.connect(SERVER_URL) as websocket:
                    async for message in websocket:
                        data = json.loads(message)
                        client_id = data["client_id"]
                        text = data["text"]
                        is_final = data["is_final"]

                        # Track active speakers
                        if client_id not in self.active_speakers:
                            self.active_speakers[client_id] = True
                            print("\n" * len(self.active_speakers))  # Add space for new speaker

                        self.print_transcription(client_id, text, is_final)

            except (websockets.ConnectionClosed, ConnectionRefusedError) as e:
                print(f"\nConnection lost: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"\nUnexpected error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

async def main():
    client = TranscriptionClient()
    try:
        await client.connect()
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")