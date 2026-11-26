import subprocess
import time
import uuid

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from config import AUDIO_DIR

app = FastAPI()
VOICE = "voices/en_US-hfc_male-medium.onnx"
MAX_AGE_SECONDS = 600

AUDIO_DIR.mkdir(exist_ok=True)


def cleanup_old_files():
    """Remove leftovers from crashes. Only files older than an hour are touched."""
    cutoff = time.time() - MAX_AGE_SECONDS
    for f in AUDIO_DIR.glob("*.wav"):
        if f.stat().st_mtime < cutoff:
            f.unlink(missing_ok=True)


cleanup_old_files()


class Say(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/speak")
def speak(body: Say, background: BackgroundTasks):
    """Creates a temporary speech file with Piper, sends it, then deletes it."""
    cleanup_old_files()
    out_path = AUDIO_DIR / f"{uuid.uuid4().hex}.wav"
    try:
        subprocess.run(
            ["piper", "--model", VOICE, "--output_file", str(out_path)],
            input=body.text.encode(),
            check=True,
            timeout=60,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        out_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Speech engine failed")

    # background.add_task(out_path.unlink, missing_ok=True)
    return FileResponse(out_path, media_type="audio/wav")