import requests
from typing import Dict, Optional


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"


def run_inference(model_id: str, prompt: str) -> Dict[str, Optional[str]]:
    """
    Run a single, stateless inference call against Ollama.
    """

    payload = {
        "model": model_id,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json=payload,
            timeout=60,
        )
    except requests.RequestException as exc:
        return {
            "success": False,
            "output": None,
            "error": f"Failed to contact Ollama service: {exc}",
        }

    if response.status_code != 200:
        return {
            "success": False,
            "output": None,
            "error": f"Ollama returned HTTP {response.status_code}",
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "success": False,
            "output": None,
            "error": "Invalid JSON response from Ollama",
        }

    output_text = data.get("response")
    if not output_text:
        return {
            "success": False,
            "output": None,
            "error": "Ollama response missing 'response' field",
        }

    return {
        "success": True,
        "output": output_text,
        "error": None,
    }
