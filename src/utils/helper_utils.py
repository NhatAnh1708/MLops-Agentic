import os
import platform


def get_chrome_path() -> str:
    """
    Returns the most common Chrome executable path based on the operating system.
    Raises:
        FileNotFoundError: If Chrome is not found in the expected path.
    """
    system = platform.system()

    if system == "Windows":
        # Common installation path for Windows
        chrome_path = os.path.join(
            os.environ.get("PROGRAMFILES", "C:\\Program Files"),
            "Google\\Chrome\\Application\\chrome.exe",
        )
    elif system == "Darwin":
        # Common installation path for macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif system == "Linux":
        # Common installation path for Linux
        chrome_path = "/usr/bin/google-chrome"
    else:
        raise FileNotFoundError(f"Unsupported operating system: {system}")

    # Verify that the Chrome executable exists at the determined path
    if not os.path.exists(chrome_path):
        raise FileNotFoundError(f"Google Chrome executable not found at: {chrome_path}")

    return chrome_path
