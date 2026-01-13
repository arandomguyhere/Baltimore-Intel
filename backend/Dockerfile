FROM python:3.11-slim

# Install ffmpeg for audio capture
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY transcribe_server.py .

# Expose WebSocket port
EXPOSE 8765

# Environment variables
ENV TRANSCRIBE_HOST=0.0.0.0
ENV TRANSCRIBE_PORT=8765
ENV WHISPER_MODEL=base

CMD ["python", "transcribe_server.py"]
