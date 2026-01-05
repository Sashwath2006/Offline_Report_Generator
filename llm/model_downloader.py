import socket
import requests
from typing import Dict


OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
OLLAMA_PULL_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/pull"


def _is_online(timeout: float = 2.0) -> bool:
    """
    Check basic network availability.
    This does NOT mean internet access, only that networking is up.
    """
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False


def download_model(ollama_id: str) -> Dict[str, str | bool]:
    """
    Explicitly download an Ollama model by ID.
    """
    if not _is_online():
        return {
            "success": False,
            "message": "Offline mode detected. Model download blocked.",
        }

    try:
        response = requests.post(
            OLLAMA_PULL_URL,
            json={"name": ollama_id},
            timeout=10,
        )
    except requests.RequestException as exc:
        return {
            "success": False,
            "message": f"Failed to contact Ollama service: {exc}",
        }

    if response.status_code != 200:
        return {
            "success": False,
            "message": f"Ollama returned HTTP {response.status_code}",
        }

    return {
        "success": True,
        "message": f"Model '{ollama_id}' download initiated successfully.",
    }
