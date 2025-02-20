from dotenv import load_dotenv
from browser_use.browser.views import BrowserState
from browser_use.agent.views import AgentOutput
from redis import Redis
import json
from loguru import logger

load_dotenv()
redis_client = Redis(host="localhost", port=6379, db=0)

def base64_to_image(base64_string: str, output_filename: str):
    """Convert base64 string to image."""
    import base64
    import os

    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))

    img_data = base64.b64decode(base64_string)
    with open(output_filename, "wb") as f:
        f.write(img_data)
    return output_filename


def cleanup_screenshots():
    import shutil
    import os

    screenshots_dir = "frontend/screenshots"
    if os.path.exists(screenshots_dir):
        shutil.rmtree(screenshots_dir)
