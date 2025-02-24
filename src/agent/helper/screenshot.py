from dotenv import load_dotenv

load_dotenv()


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
    import os
    import shutil

    screenshots_dir = "frontend/screenshots"
    if os.path.exists(screenshots_dir):
        shutil.rmtree(screenshots_dir)
