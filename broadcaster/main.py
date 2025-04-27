import asyncio
import json
import os
import sys
import uuid
import wave
from typing import Optional

import pyaudio
import websockets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Audio configuration
CHUNK_SIZE = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000  # Required by Whisper
SERVER_URL = os.getenv('SERVER_URL', 'ws://localhost:8000/audio')

class AudioBroadcaster:
    def __init__(self):
        self.client_id = str(uuid.uuid4())
        self.p = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.websocket = None
        self.is_running = False

    async def connect(self):
        while True:
            try:
                async with websockets.connect(SERVER_URL) as ws:
                    self.websocket = ws
                    await self.send_client_info()
                    await self.stream_audio()
            except (websockets.ConnectionClosed, ConnectionRefusedError) as e:
                print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    async def send_client_info(self):
        info = {
            "client_id": self.client_id,
            "sample_rate": RATE,
            "channels": CHANNELS
        }
        await self.websocket.send(json.dumps(info))

    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.websocket and self.websocket.open:
            asyncio.create_task(self.websocket.send(in_data))
        return (in_data, pyaudio.paContinue)

    async def stream_audio(self):
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=self.audio_callback
        )
        
        self.stream.start_stream()
        self.is_running = True
        
        try:
            while self.is_running and self.stream.is_active():
                await asyncio.sleep(0.1)
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()

    def cleanup(self):
        self.is_running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

async def main():
    broadcaster = AudioBroadcaster()
    try:
        await broadcaster.connect()
    except KeyboardInterrupt:
        print("\nStopping broadcaster...")
    finally:
        broadcaster.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")