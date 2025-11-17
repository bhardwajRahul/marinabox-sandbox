import subprocess
import base64
import os
from fastapi import FastAPI, HTTPException
from computer_use_server.api_v2.utils import get_video_size_from_env
from computer_use_server.api_v2.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


DISPLAY_NUM = os.getenv("DISPLAY_NUM", "99")
DISPLAY_ENV = os.environ.copy()
DISPLAY_ENV["DISPLAY"] = f":{DISPLAY_NUM}"

app = FastAPI()

@app.get("/screenshot")
async def get_screenshot():
    try:
        video_size = get_video_size_from_env()
        logger.info(f"Preparing to take screenshot at {video_size} on DISPLAY=:{DISPLAY_NUM}")

        screenshot_path = "/tmp/screenshot.png"
        cmd = [
        "ffmpeg",
        "-hide_banner", "-loglevel", "info",
        "-f", "x11grab", "-video_size", video_size,
        "-i", f":{DISPLAY_NUM}",
        "-frames:v", "1",
        "-update", "1",
        "-y", screenshot_path,
        ]

        result = subprocess.run(
            cmd,
            check=True,
            env=DISPLAY_ENV,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        logger.debug(f"Screenshot command output: {result.stdout}")
        logger.debug(f"Screenshot command stderr: {result.stderr}")


        with open(screenshot_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        os.remove(screenshot_path)
        
        result = {"status": "success", "image": encoded_string}
        logger.info("Screenshot captured successfully")
        return result
    except Exception as e:
        logger.exception("Failed to capture screenshot")
        raise HTTPException(status_code=500, detail=str(e))