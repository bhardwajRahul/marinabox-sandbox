import subprocess
import base64
import os
from fastapi import FastAPI, HTTPException
from computer_use_server.api_v2.utils import get_video_size_from_env
from computer_use_server.api_v2.logging_config import setup_logging
from computer_use_server.api_v2.models import Coordinates, TextInput
import logging

setup_logging()
logger = logging.getLogger(__name__)

DISPLAY_NUM = os.getenv("DISPLAY_NUM", "99")
DISPLAY_ENV = os.environ.copy()
DISPLAY_ENV["DISPLAY"] = f":{DISPLAY_NUM}"

# Typing behavior
TYPING_DELAY_MS = 12
TYPING_GROUP_SIZE = 50

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
        logger.info(f"Captured mouse position: {x}, {y}")
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
		logger.info(f"Moved mouse to ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
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
		logger.info(f"Performed left click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
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
		logger.info(f"Performed right click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		return {"status": "success", "x": x, "y": y}
	except Exception as e:
		logger.exception("Failed to perform right click")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/middle_click")
async def middle_click(coords: Coordinates):
	try:
		x = int(coords.x)
		y = int(coords.y)
		logger.info(f"Middle click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		# Move first, then click
		move_cmd = ["xdotool", "mousemove", "--sync", str(x), str(y)]
		click_cmd = ["xdotool", "click", "2"]
		move_result = subprocess.run(
			move_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Mouse move before middle click stdout: {move_result.stdout}")
		logger.debug(f"Mouse move before middle click stderr: {move_result.stderr}")
		click_result = subprocess.run(
			click_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Middle click stdout: {click_result.stdout}")
		logger.debug(f"Middle click stderr: {click_result.stderr}")
		logger.info(f"Performed middle click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		return {"status": "success", "x": x, "y": y}
	except Exception as e:
		logger.exception("Failed to perform middle click")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/double_click")
async def double_click(coords: Coordinates):
	try:
		x = int(coords.x)
		y = int(coords.y)
		logger.info(f"Double click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		# Move first, then double-click
		move_cmd = ["xdotool", "mousemove", "--sync", str(x), str(y)]
		click_cmd = ["xdotool", "click", "--repeat", "2", "--delay", "500", "1"]
		move_result = subprocess.run(
			move_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Mouse move before double click stdout: {move_result.stdout}")
		logger.debug(f"Mouse move before double click stderr: {move_result.stderr}")
		click_result = subprocess.run(
			click_cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Double click stdout: {click_result.stdout}")
		logger.debug(f"Double click stderr: {click_result.stderr}")
		logger.info(f"Performed double click at ({x}, {y}) on DISPLAY=:{DISPLAY_NUM}")
		return {"status": "success", "x": x, "y": y}
	except Exception as e:
		logger.exception("Failed to perform double click")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/key")
async def send_key(input: TextInput):
	try:
		if not input.text:
			raise HTTPException(status_code=400, detail="text is required")
		logger.info(f"Sending key '{input.text}' on DISPLAY=:{DISPLAY_NUM}")
		cmd = ["xdotool", "key", "--", input.text]
		result = subprocess.run(
			cmd,
			check=True,
			env=DISPLAY_ENV,
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		)
		logger.debug(f"Key stdout: {result.stdout}")
		logger.debug(f"Key stderr: {result.stderr}")
		logger.info(f"Sent key '{input.text}' on DISPLAY=:{DISPLAY_NUM}")
		return {"status": "success"}
	except Exception as e:
		logger.exception("Failed to send key")
		raise HTTPException(status_code=500, detail=str(e))

@app.post("/type")
async def type_text(input: TextInput):
	try:
		if not input.text:
			raise HTTPException(status_code=400, detail="text is required")
		logger.info(f"Typing {len(input.text)} characters on DISPLAY=:{DISPLAY_NUM}")
		for i in range(0, len(input.text), TYPING_GROUP_SIZE):
			chunk = input.text[i:i + TYPING_GROUP_SIZE]
			cmd = ["xdotool", "type", "--delay", str(TYPING_DELAY_MS), "--", chunk]
			result = subprocess.run(
				cmd,
				check=True,
				env=DISPLAY_ENV,
				text=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
			)
			logger.debug(f"Type chunk stdout: {result.stdout}")
			logger.debug(f"Type chunk stderr: {result.stderr}")
		logger.info(f"Typed {input.text} on DISPLAY=:{DISPLAY_NUM}")
		return {"status": "success"}
	except Exception as e:
		logger.exception("Failed to type text")
		raise HTTPException(status_code=500, detail=str(e))