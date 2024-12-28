import time
import os
import logging
from dotenv import load_dotenv
from core.home_assistant import HomeAssistant
from extras.fortnite_connector import FortniteConnector

# Load environment variables from .env
load_dotenv()

HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
FORTNITE_USERNAME = os.getenv("FORTNITE_USERNAME")

# Check if environment variables are set
if not all([HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN, FORTNITE_USERNAME]):
    raise ValueError("Missing required environment variables!")

light_id = "light.your_light_id"  # Change this to your light entity ID

# Setup logging
logging.basicConfig(level=logging.INFO)

def breathing_effect(home_assistant, light_id, color, duration, loop_time=0.6):
    """
    Function to create a breathing effect with pulsing brightness.
    """
    for i in range(int(duration / loop_time)):
        brightness = 255 if i % 2 != 0 else 30
        home_assistant.change_color(light_id=light_id, color=color, brightness=brightness, transition=loop_time)
        time.sleep(loop_time)  # Control the speed of the pulse (adjust sleep time for slower or faster pulse)
    home_assistant.change_color(light_id=light_id, color=(255, 255, 255), brightness=255, transition=1)

def on_kill_function(home_assistant):
    try:
        home_assistant.change_color(light_id=light_id, color=(0, 255, 0), brightness=255, transition=0.2)
        time.sleep(0.5)
        home_assistant.change_color(light_id=light_id, color=(255, 255, 255), brightness=255, transition=1)
        logging.info("Kill event: light changed to green and reset.")
    except Exception as e:
        logging.error(f"Error in on_kill_function: {e}")

def on_death_function(home_assistant):
    try:
        # Set light to red with full brightness
        home_assistant.change_color(light_id=light_id, color=(255, 0, 0), brightness=255, transition=1)
        logging.info("Death event: light changed to red.")
        breathing_effect(home_assistant, light_id, (255, 0, 0), duration=7)
    except Exception as e:
        logging.error(f"Error in on_death_function: {e}")

def on_ko_function(home_assistant):
    try:
        # Set light to red-orange with full brightness
        home_assistant.change_color(light_id=light_id, color=(255, 127, 0), brightness=255, transition=1)
        logging.info("KO event: light changed to red-orange.")
        breathing_effect(home_assistant, light_id, (255, 127, 0), duration=3)
    except Exception as e:
        logging.error(f"Error in on_ko_function: {e}")



def main():
    try:
        # Initialize Home Assistant and LightBinder
        home_assistant = HomeAssistant(HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN)

        fortnite_connector = FortniteConnector(os.path.expandvars(r"%LOCALAPPDATA%\FortniteGame\Saved\Logs\FortniteGame.log"), fortnite_username=FORTNITE_USERNAME)

        fortnite_connector.on_events_functions["kill"] = lambda: on_kill_function(home_assistant)
        fortnite_connector.on_events_functions["death"] = lambda: on_death_function(home_assistant)
        fortnite_connector.on_events_functions["ko"] = lambda: on_ko_function(home_assistant)


        # Monitor Fortnite logs
        fortnite_connector.monitor_logs()

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
