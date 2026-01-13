#!/usr/bin/env python3
"""
Scanner Transcription WebSocket Server

Connects to Broadcastify audio streams, transcribes using Whisper,
and pushes real-time transcripts to connected dashboard clients.
"""

import asyncio
import json
import os
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import websockets
except ImportError:
    print("Installing websockets...")
    subprocess.run(["pip", "install", "websockets"], check=True)
    import websockets

try:
    import whisper
except ImportError:
    print("Installing openai-whisper...")
    subprocess.run(["pip", "install", "openai-whisper"], check=True)
    import whisper

# Configuration
HOST = os.getenv("TRANSCRIBE_HOST", "0.0.0.0")
PORT = int(os.getenv("TRANSCRIBE_PORT", "8765"))
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large

# Broadcastify feed URLs (requires ffmpeg to capture)
BROADCASTIFY_FEEDS = {
    43356: "Baltimore Terminal RR",
    14954: "CSX/NS Regional",
    42710: "Baltimore Marine",
    31547: "Coast Guard Sector"
}

# Global state
connected_clients = set()
active_transcriptions = {}  # feed_id -> task
model = None


def get_broadcastify_stream_url(feed_id):
    """
    Get the audio stream URL for a Broadcastify feed.
    Note: Broadcastify requires authentication for some streams.
    """
    # Public stream URL pattern (may require Broadcastify premium for some feeds)
    return f"https://broadcastify.cdnstream1.com/{feed_id}"


async def capture_and_transcribe(feed_id, feed_name):
    """Capture audio from Broadcastify and transcribe in chunks."""
    global model

    stream_url = get_broadcastify_stream_url(feed_id)

    # Create temp directory for audio chunks
    with tempfile.TemporaryDirectory() as tmpdir:
        chunk_path = Path(tmpdir) / "chunk.wav"
        chunk_duration = 10  # seconds per chunk

        while feed_id in active_transcriptions:
            try:
                # Use ffmpeg to capture audio chunk
                process = await asyncio.create_subprocess_exec(
                    "ffmpeg",
                    "-y",
                    "-i", stream_url,
                    "-t", str(chunk_duration),
                    "-acodec", "pcm_s16le",
                    "-ar", "16000",
                    "-ac", "1",
                    str(chunk_path),
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )

                await asyncio.wait_for(process.wait(), timeout=chunk_duration + 10)

                if chunk_path.exists() and chunk_path.stat().st_size > 1000:
                    # Transcribe the chunk
                    result = model.transcribe(
                        str(chunk_path),
                        language="en",
                        fp16=False
                    )

                    text = result.get("text", "").strip()

                    if text and len(text) > 3:  # Filter out noise
                        transcript = {
                            "type": "transcript",
                            "feed_id": feed_id,
                            "feed_name": feed_name,
                            "text": text,
                            "timestamp": datetime.utcnow().isoformat()
                        }

                        # Broadcast to all connected clients
                        await broadcast(transcript)

            except asyncio.TimeoutError:
                print(f"Timeout capturing from feed {feed_id}")
            except Exception as e:
                print(f"Error transcribing feed {feed_id}: {e}")
                await asyncio.sleep(2)


async def broadcast(message):
    """Send message to all connected clients."""
    if connected_clients:
        msg = json.dumps(message)
        await asyncio.gather(
            *[client.send(msg) for client in connected_clients],
            return_exceptions=True
        )


async def handle_client(websocket, path):
    """Handle a WebSocket client connection."""
    connected_clients.add(websocket)
    client_id = id(websocket)
    print(f"Client {client_id} connected. Total clients: {len(connected_clients)}")

    try:
        # Send available feeds
        await websocket.send(json.dumps({
            "type": "feeds",
            "feeds": [
                {"id": fid, "name": name}
                for fid, name in BROADCASTIFY_FEEDS.items()
            ]
        }))

        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")
                feed_id = data.get("feed_id")

                if action == "start" and feed_id:
                    feed_id = int(feed_id)
                    if feed_id not in active_transcriptions:
                        feed_name = BROADCASTIFY_FEEDS.get(feed_id, f"Feed {feed_id}")
                        print(f"Starting transcription for {feed_name} ({feed_id})")

                        active_transcriptions[feed_id] = True
                        asyncio.create_task(capture_and_transcribe(feed_id, feed_name))

                        await websocket.send(json.dumps({
                            "type": "status",
                            "feed_id": feed_id,
                            "status": "started"
                        }))

                elif action == "stop" and feed_id:
                    feed_id = int(feed_id)
                    if feed_id in active_transcriptions:
                        del active_transcriptions[feed_id]
                        print(f"Stopped transcription for feed {feed_id}")

                        await websocket.send(json.dumps({
                            "type": "status",
                            "feed_id": feed_id,
                            "status": "stopped"
                        }))

            except json.JSONDecodeError:
                pass

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"Client {client_id} disconnected. Total clients: {len(connected_clients)}")


async def main():
    global model

    print("=" * 50)
    print("Scanner Transcription Server")
    print("=" * 50)
    print(f"Loading Whisper model: {WHISPER_MODEL}")

    model = whisper.load_model(WHISPER_MODEL)
    print(f"Model loaded successfully")

    print(f"\nStarting WebSocket server on ws://{HOST}:{PORT}")
    print(f"Available feeds: {list(BROADCASTIFY_FEEDS.values())}")
    print("-" * 50)

    async with websockets.serve(handle_client, HOST, PORT):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
