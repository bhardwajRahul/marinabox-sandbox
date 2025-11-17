import os
import logging

logger = logging.getLogger(__name__)

def get_video_size_from_env() -> str:
    """
    Derive WIDTHxHEIGHT from RESOLUTION env var.
    Accepts formats like:
      - 1920x1080x24 -> uses 1920x1080
      - 1280x800     -> uses 1280x800
    Falls back to 1280x800 if parsing fails.
    """
    logger.debug(f"Getting resolution from env")
    resolution = os.getenv("RESOLUTION", "")
    logger.debug(f"Resolution: {resolution}")
    try:
        if resolution:
            parts = resolution.split("x")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                width = parts[0]
                height = parts[1]
                return f"{width}x{height}"
    except Exception:
        logger.debug(f"Error getting resolution from env")
        raise Exception(f"Error getting resolution from env")
    return "1280x800"


