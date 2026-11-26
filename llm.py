import requests as req
from config import OLLAMA_URL, MODEL


class LLMError(Exception):
    """Raised when the model cannot give a usable reply."""


def generate(messages, tools=None):
    """Send messages to the model and return its reply message."""
    payload = {"model": MODEL, "messages": messages, "stream": False}
    if tools:
        payload["tools"] = tools

    try:
        response = req.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
    except req.ConnectionError:
        raise LLMError("Cannot reach Ollama. Is it running?") from None
    except req.Timeout:
        raise LLMError("The model took too long to answer.") from None

    if not response.ok:
        try:
            detail = response.json().get("error", response.text)
        except ValueError:
            detail = response.text
        raise LLMError(f"Ollama returned {response.status_code}: {detail}")

    try:
        return response.json()["message"]
    except (ValueError, KeyError):
        raise LLMError("Ollama sent a reply in an unexpected format.") from None