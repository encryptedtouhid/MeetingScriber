import asyncio
import json
import logging
import os
from typing import Dict, Set

import numpy as np
import torch
import websockets
import whisper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8000))

class TranscriptionServer:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.clients: Dict[str, Set[websockets.WebSocketServerProtocol]] = {
            "audio": set(),
            "transcribe": set()
        }
        self.audio_buffers: Dict[str, list] = {}
        self.processing_locks: Dict[str, asyncio.Lock] = {}

    async def register(self, websocket: websockets.WebSocketServerProtocol, client_type: str):
        self.clients[client_type].add(websocket)
        logger.info(f"New {client_type} client connected. Total {client_type} clients: {len(self.clients[client_type])}")

    async def unregister(self, websocket: websockets.WebSocketServerProtocol, client_type: str):
        self.clients[client_type].remove(websocket)
        logger.info(f"{client_type} client disconnected. Total {client_type} clients: {len(self.clients[client_type])}")

    async def process_audio(self, client_id: str):
        while True:
            if client_id in self.audio_buffers and len(self.audio_buffers[client_id]) >= 16000:  # 1 second of audio
                async with self.processing_locks[client_id]:
                    audio_data = np.concatenate(self.audio_buffers[client_id])
                    self.audio_buffers[client_id] = []

                # Convert audio to format expected by Whisper
                audio_data = torch.from_numpy(audio_data).float()
                
                # Transcribe
                result = self.model.transcribe(
                    audio_data.numpy(),
                    language='en',
                    without_timestamps=True
                )

                # Broadcast transcription to all connected clients
                if result["text"].strip():
                    message = {
                        "client_id": client_id,
                        "text": result["text"].strip(),
                        "is_final": True
                    }
                    await self.broadcast_transcription(message)
            
            await asyncio.sleep(0.1)

    async def broadcast_transcription(self, message: dict):
        if not self.clients["transcribe"]:
            return

        encoded_message = json.dumps(message)
        await asyncio.gather(
            *[client.send(encoded_message) for client in self.clients["transcribe"]]
        )

    async def handle_audio_client(self, websocket: websockets.WebSocketServerProtocol):
        try:
            # Get client information
            client_info = json.loads(await websocket.recv())
            client_id = client_info["client_id"]
            
            # Initialize client buffers and locks
            self.audio_buffers[client_id] = []
            self.processing_locks[client_id] = asyncio.Lock()
            
            # Start processing task
            process_task = asyncio.create_task(self.process_audio(client_id))
            
            await self.register(websocket, "audio")
            
            try:
                async for message in websocket:
                    # Convert binary audio data to numpy array
                    audio_chunk = np.frombuffer(message, dtype=np.float32)
                    self.audio_buffers[client_id].append(audio_chunk)
            finally:
                await self.unregister(websocket, "audio")
                process_task.cancel()
                
                # Cleanup client resources
                if client_id in self.audio_buffers:
                    del self.audio_buffers[client_id]
                if client_id in self.processing_locks:
                    del self.processing_locks[client_id]
                
        except Exception as e:
            logger.error(f"Error in audio client handler: {e}")

    async def handle_transcription_client(self, websocket: websockets.WebSocketServerProtocol):
        try:
            await self.register(websocket, "transcribe")
            try:
                await websocket.wait_closed()
            finally:
                await self.unregister(websocket, "transcribe")
        except Exception as e:
            logger.error(f"Error in transcription client handler: {e}")

    async def start(self):
        async with websockets.serve(
            lambda ws, path: self.handle_audio_client(ws) if path == "/audio" 
            else self.handle_transcription_client(ws),
            HOST,
            PORT
        ):
            logger.info(f"Server started on ws://{HOST}:{PORT}")
            await asyncio.Future()  # run forever

if __name__ == "__main__":
    server = TranscriptionServer()
    asyncio.run(server.start())