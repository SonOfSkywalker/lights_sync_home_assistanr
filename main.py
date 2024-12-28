import time
import yaml
import os
from dotenv import load_dotenv
from core.home_assistant import HomeAssistant
from core.light_binding import LightBinder
from config.constants import MONITORS

# Load environment variables from .env
load_dotenv()

HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
CONFIG_PATH = os.getenv("CONFIG_PATH")

def main():
    # Load light configurations from a YAML file
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    # Initialize Home Assistant and LightBinder
    home_assistant = HomeAssistant(HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN)
    light_binder = LightBinder(home_assistant)

    brightness_boost = config.get("brightness_boost", 1.5)

    # Update lights at 10 FPS
    while True:
        for monitor in MONITORS.keys():
            if monitor in config["monitors"]:
                light_binder.bind_lights(
                    lights_config=config["monitors"][monitor]["lights"],
                    monitor_number=MONITORS[monitor],
                    brightness_boost=brightness_boost,
                )

        time.sleep(1 / config.get("number_of_updates_per_second", 10))

if __name__ == "__main__":
    main()
