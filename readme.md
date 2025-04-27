# MeetingScriber

A real-time speech-to-text system that transcribes audio using OpenAI's Whisper model locally. The system consists of three microservices that work together to capture, process, and display transcriptions in real-time.

## Architecture

The system consists of three main services:

1. **Broadcaster**: Captures microphone audio and streams it over WebSocket
2. **Server**: Processes audio using Whisper and broadcasts transcriptions
3. **Client**: Displays real-time transcriptions from connected broadcasters

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher (for local development)
- A microphone for audio capture
- Operating System: macOS, Windows, or Linux

## Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MeetingScriber.git
   cd MeetingScriber
   ```

2. Build and start the services:
   ```bash
   docker-compose up --build
   ```

## Manual Installation

### 1. Set up Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install the Broadcaster Service

#### macOS
```bash
sudo ./install_scripts/macos/install_broadcaster.sh
```

#### Linux
```bash
sudo ./install_scripts/linux/install_broadcaster.sh
```

#### Windows
```bash
.\install_scripts\windows\install_broadcaster.bat
```

### 3. Start the Server
```bash
python server/main.py
```

### 4. Start the Client
```bash
python client/main.py
```

## Project Structure

```
├── broadcaster/           # Audio capture service
│   ├── main.py           # Main broadcaster logic
│   └── service/          # Platform-specific service files
├── server/               # Whisper transcription service
│   ├── main.py          # WebSocket server & transcription
│   └── Dockerfile
├── client/              # Transcription display service
│   ├── main.py         # Client UI
│   └── Dockerfile
├── docker-compose.yml   # Docker services configuration
├── requirements.txt     # Python dependencies
└── install_scripts/     # Platform-specific installers
```

## Configuration

Default ports and settings can be modified in `.env`:
- Broadcaster → Server: `ws://server:8000/audio`
- Server → Client: `ws://server:8000/transcribe`

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

## License

MIT License