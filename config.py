import os
from pathlib import Path

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:3b"
MAX_MESSAGES = 20
TTS_URL = "http://localhost:8001"
VOICE_ENABLED = os.getenv("ALFRED_VOICE", "1") == "1"
AUDIO_DIR = Path(__file__).parent / "audio_tmp"
DB_PATH = "alfred.db"
USER_COLOR = "cyan"
ALFRED_COLOR = "yellow"