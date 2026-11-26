import subprocess
import sys
import uuid

import requests

from config import AUDIO_DIR, TTS_URL, VOICE_ENABLED

enabled = VOICE_ENABLED


def set_enabled(value):
    """Turn voice on or off while the assistant is running."""
    global enabled
    enabled = value


def play(path):
    """Play a WAV file and wait until it finishes."""
    if sys.platform == "win32":
        import winsound
        winsound.PlaySound(path, winsound.SND_FILENAME)
    elif sys.platform == "darwin":
        subprocess.run(["afplay", path])
    else:
        subprocess.run(["aplay", path])


def speak(text):
    """Speak text aloud. Does nothing if voice is off or the service is down."""
    if not enabled:
        return

    try:
        response = requests.post(f"{TTS_URL}/speak", json={"text": text}, timeout=60)
        response.raise_for_status()
    except requests.RequestException:
        return

    AUDIO_DIR.mkdir(exist_ok=True)
    path = AUDIO_DIR / f"{uuid.uuid4().hex}.wav"
    path.write_bytes(response.content)
    try:
        play(str(path))
    finally:
        path.unlink(missing_ok=True)  # deleted even if playback fails