from typing import List, Dict


def get_model_registry() -> List[Dict]:
    """
    Returns the static registry of supported LLM models.
    """
    return [
        {
            "name": "LLaMA 3 8B",
            "ollama_id": "llama3:8b",
            "min_ram_gb": 16.0,
            "min_vram_gb": 8.0,
            "gpu_required": True,
            "purpose": "High-quality security reasoning on capable GPUs",
        },
        {
            "name": "Mistral 7B",
            "ollama_id": "mistral:7b",
            "min_ram_gb": 16.0,
            "min_vram_gb": None,
            "gpu_required": False,
            "purpose": "Balanced reasoning for CPU-only or low-VRAM systems",
        },
        {
            "name": "Gemma 7B",
            "ollama_id": "gemma:7b",
            "min_ram_gb": 12.0,
            "min_vram_gb": None,
            "gpu_required": False,
            "purpose": "Lightweight reasoning for constrained environments",
        },
    ]


def recommend_models(hardware: dict) -> List[Dict]:
    """
    Recommend models based on detected hardware.
    """
    registry = get_model_registry()
    recommendations: List[Dict] = []

    total_ram = hardware["ram"]["total_gb"]
    gpu_info = hardware["gpu"]

    for model in registry:
        # RAM check
        if total_ram < model["min_ram_gb"]:
            continue

        # GPU-required model checks
        if model["gpu_required"]:
            if not gpu_info["available"]:
                continue
            if model["min_vram_gb"] is not None:
                if gpu_info["vram_gb"] is None:
                    continue
                if gpu_info["vram_gb"] < model["min_vram_gb"]:
                    continue

        recommendations.append(model)

    return recommendations
