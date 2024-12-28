import mss
from PIL import Image

class ScreenCapture:
    @staticmethod
    def capture_monitor(monitor_number=1):
        """Capture the specified monitor's screen as a PIL image."""
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_number]
            screenshot = sct.grab(monitor)
            return Image.frombytes("RGB", screenshot.size, screenshot.rgb)
