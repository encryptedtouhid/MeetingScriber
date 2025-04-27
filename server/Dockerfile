FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Whisper model during build
RUN python -c "import whisper; whisper.load_model('base')"

# Copy server code
COPY . .

# Expose WebSocket port
EXPOSE 8000

CMD ["python", "-u", "main.py"]