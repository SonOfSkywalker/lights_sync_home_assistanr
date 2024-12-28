import os
from dotenv import load_dotenv
import numpy as np
from PIL import Image
import mss
import requests
import yaml

# Load environment variables from .env
load_dotenv()

# Retrieve sensitive information from environment variables
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
CONFIG_PATH = os.getenv("CONFIG_PATH")

AREAS = {
    "whole_screen": -1,
    "top_left": 0,
    "top_right": 1,
    "bottom_left": 2,
    "bottom_right": 3,
}

# TWO MONITORS SETUP
MONITORS = {
    "main": 1,
    "secondary": 2,
}


def capture_monitor(monitor_number=1):
    """Capture the specified monitor's screen as a PIL image."""
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_number]
        screenshot = sct.grab(monitor)
        return Image.frombytes("RGB", screenshot.size, screenshot.rgb)


def calculate_average_color(image, box):
    """Calculate the average color and brightness of a specific region."""
    cropped = image.crop(box)
    pixels = np.array(cropped)
    avg_color = tuple(np.mean(pixels, axis=(0, 1)).astype(int))
    brightness = int(
        np.mean(
            0.299 * pixels[..., 0] + 0.587 * pixels[..., 1] + 0.114 * pixels[..., 2]
        )
    )
    return avg_color, brightness


def get_average_colors(image):
    """Compute average colors and brightness for 4 quadrants of a given image."""
    w, h = image.size
    quadrants = [
        (0, 0, w // 2, h // 2),
        (w // 2, 0, w, h // 2),
        (0, h // 2, w // 2, h),
        (w // 2, h // 2, w, h),
    ]
    avg_data = [calculate_average_color(image, quad) for quad in quadrants]
    avg_colors = np.array([data[0] for data in avg_data])
    avg_brightness = np.array([data[1] for data in avg_data])
    return avg_colors, avg_brightness


def change_color(light_id, color, brightness, transition=0.2):
    """
    Change the color and brightness of a light in Home Assistant with a smooth transition.

    Parameters:
        light_id (str): The entity ID of the light (e.g., "light.hue_go_2_bureau").
        color (tuple): The RGB color as a tuple (e.g., (255, 0, 0) for red).
        brightness (int): The brightness level (0-255).
        transition (float): Duration of the color transition in seconds.

    Returns:
        dict: The response from the Home Assistant API.
    """
    headers = {
        "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "entity_id": light_id,
        "rgb_color": list(map(int, color)),
        "brightness": int(brightness),
        "transition": transition,
    }

    try:
        response = requests.post(HOME_ASSISTANT_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def bind_lights(lights_config, monitor_number=1, brightness_boost=1.5):
    """Bind multiple lights to the average colors and brightness of a monitor's screen."""
    # Capture the screen and calculate average colors and brightness
    screen = capture_monitor(monitor_number)
    avg_colors, avg_brightness = get_average_colors(screen)

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
        change_color(light_id, color, brightness)


if __name__ == "__main__":
    import time

    # Load light configurations from a YAML file
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    brightness_boost = config.get("brightness_boost", 1.5)

    # Update lights at 10 FPS
    while True:
        for monitor in MONITORS.keys():
            if monitor in config["monitors"]:
                bind_lights(
                    lights_config=config["monitors"][monitor]["lights"],
                    monitor_number=MONITORS[monitor],
                    brightness_boost=brightness_boost,
                )

        time.sleep(1 / config.get("number_of_updates_per_second", 10))
