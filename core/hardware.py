import platform
import psutil


def detect_hardware() -> dict:
    """
    Detect system hardware in a deterministic, offline-safe manner.

    Returns:
        dict: Hardware information with fixed schema.
    """

    cpu_info = {
        "model": platform.processor() or platform.uname().processor,
        "cores": psutil.cpu_count(logical=False) or 0,
        "threads": psutil.cpu_count(logical=True) or 0,
    }

    ram_info = {
        "total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 1)
    }

    gpu_info = {
        "available": False,
        "vendor": None,
        "model": None,
        "vram_gb": None,
    }

    # Optional GPU detection via torch (if installed)
    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            gpu_info = {
                "available": True,
                "vendor": "NVIDIA",
                "model": props.name,
                "vram_gb": round(props.total_memory / (1024 ** 3), 1),
            }
    except ImportError:
        # Torch not installed — GPU remains unavailable
        pass
    except Exception:
        # Any unexpected GPU error must not crash the app
        pass

    return {
        "cpu": cpu_info,
        "ram": ram_info,
        "gpu": gpu_info,
    }
