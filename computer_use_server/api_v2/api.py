import subprocess
import base64
import os
from fastapi import FastAPI, HTTPException
from computer_use_server.api_v2.utils import get_video_size_from_env
from computer_use_server.api_v2.logging_config import setup_logging
from computer_use_server.api_v2.models import Coordinates
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

@app.get("/mouse_position")
async def get_mouse_position():
    try:
        cmd = ["xdotool", "getmouselocation", "--shell"]
        result = subprocess.run(
            cmd,
            check=True,
            env=DISPLAY_ENV,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        logger.debug(f"result after running xdotool getmouselocation --shell: {result}")
        logger.debug(f"Mouse position stdout: {result.stdout}")
        logger.debug(f"Mouse position stderr: {result.stderr}")

        lines = [line for line in result.stdout.strip().split("\n") if "=" in line]
        location_data = dict(line.split("=", 1) for line in lines)
        x = int(location_data["X"])
        y = int(location_data["Y"])
        return {"status": "success", "x": x, "y": y}
    except Exception as e:
        logger.exception("Failed to get mouse position")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mouse_move")
async def mouse_move(coords: Coordinates):
	try:
		x = int(coords.x)
		y = int(coords.y)
		logger.info(f"Moving mouse to ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		cmd = ["xdotool", "mousemove", "--sync", str(x), str(y)]
		result = subprocess.run(
			cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Mouse move stdout: {result.stdout}")
		logger.debug(f"Mouse move stderr: {result.stderr}")
		return {"status": "success", "x": x, "y": y}
	except Exception as e:
		logger.exception("Failed to move mouse")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/left_click")
async def left_click(coords: Coordinates):
	try:
		x = int(coords.x)
		y = int(coords.y)
		logger.info(f"Left click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		# Move first, then click
		move_cmd = ["xdotool", "mousemove", "--sync", str(x), str(y)]
		click_cmd = ["xdotool", "click", "1"]
		move_result = subprocess.run(
			move_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Mouse move before left click stdout: {move_result.stdout}")
		logger.debug(f"Mouse move before left click stderr: {move_result.stderr}")
		click_result = subprocess.run(
			click_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Left click stdout: {click_result.stdout}")
		logger.debug(f"Left click stderr: {click_result.stderr}")
		return {"status": "success", "x": x, "y": y}
	except Exception as e:
		logger.exception("Failed to perform left click")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/right_click")
async def right_click(coords: Coordinates):
	try:
		x = int(coords.x)
		y = int(coords.y)
		logger.info(f"Right click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		# Move first, then click
		move_cmd = ["xdotool", "mousemove", "--sync", str(x), str(y)]
		click_cmd = ["xdotool", "click", "3"]
		move_result = subprocess.run(
			move_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Mouse move before right click stdout: {move_result.stdout}")
		logger.debug(f"Mouse move before right click stderr: {move_result.stderr}")
		click_result = subprocess.run(
			click_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Right click stdout: {click_result.stdout}")
		logger.debug(f"Right click stderr: {click_result.stderr}")
		return {"status": "success", "x": x, "y": y}
	except Exception as e:
		logger.exception("Failed to perform right click")
		raise HTTPException(status_code=500, detail=str(e))