import numpy as np
from core.color_processing import ColorProcessor
from core.screen_capture import ScreenCapture
from config.constants import AREAS

class LightBinder:
    def __init__(self, home_assistant):
        self.home_assistant = home_assistant

    def bind_lights(self, lights_config, monitor_number=1, brightness_boost=1.5):
        """Bind multiple lights to the average colors and brightness of a monitor's screen."""
        # Capture the screen and calculate average colors and brightness
        screen = ScreenCapture.capture_monitor(monitor_number)
        avg_colors, avg_brightness = ColorProcessor.get_average_colors(screen)

        # Normalize brightness to fit the 0-255 range for Home Assistant and apply the boost
        normalized_brightness = np.clip(
            (avg_brightness / 255 * 200 * brightness_boost), 0, 255
        ).astype(int)

        # Apply average colors and brightness to the lights
        for config in lights_config:
            light_id = config["light_id"]
            screen_area = config["screen_area"]
            area_number = AREAS.get(screen_area)
            if area_number in [-1, None]:
                color = avg_colors.mean(axis=0).astype(int)
                brightness = int(normalized_brightness.mean())
            else:
                color = avg_colors[area_number]
                brightness = normalized_brightness[area_number]
            self.home_assistant.change_color(light_id, color, brightness)
