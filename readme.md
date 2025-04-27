# MeetingScriber

A real-time speech-to-text system that transcribes audio using OpenAI's Whisper model locally. The system consists of three microservices that work together to capture, process, and display transcriptions in real-time.

## Architecture

The system consists of three main services:

1. **Broadcaster**: Captures microphone audio and streams it over WebSocket
2. **Server**: Processes audio using Whisper and broadcasts transcriptions
3. **Client**: Displays real-time transcriptions from connected broadcasters

## Prerequisites

- Python 3.9 or higher
- A microphone for audio capture
- Operating System: macOS, Windows, or Linux

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/encryptedtouhid/MeetingScriber.git
cd MeetingScriber
```

### 2. Set up Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install components based on your needs:

# For all components
pip install -r requirements.txt

# For server only
pip install -r server/requirements.txt

# For client only
pip install -r client/requirements.txt

# For broadcaster only
pip install -r broadcaster/requirements.txt
```

### 3. Install the Broadcaster Service

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

## Running the Services

### 1. Start the Server
```bash
python server/main.py
```

### 2. Start the Client
```bash
python client/main.py
```

The broadcaster service will start automatically after installation.

## Project Structure

```
├── broadcaster/           # Audio capture service
│   ├── main.py           # Main broadcaster logic
│   └── service/          # Platform-specific service files
├── server/               # Whisper transcription service
│   └── main.py          # WebSocket server & transcription
├── client/              # Transcription display service
│   └── main.py         # Client UI
├── requirements.txt     # Python dependencies
└── install_scripts/     # Platform-specific installers
```

## Configuration

Default WebSocket connections:
- Broadcaster → Server: `ws://localhost:8000/audio`
- Server → Client: `ws://localhost:8000/transcribe`

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

## Troubleshooting

### SSL Certificate Issues (macOS)
If you encounter SSL certificate errors when downloading the Whisper model, try:
```bash
pip install --upgrade certifi
export SSL_CERT_FILE="$(python -m certifi)"
```

### WebSocket Connection Issues
- Ensure the server is running before starting the client
- Check if ports are not blocked by firewall
- Default ports can be modified in each service's configuration

## License

MIT License