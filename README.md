# Sync Home Assistant Lights to your monitors

Creates an Ambilight effect by syncing Home Assistant lights with your monitor’s colors and brightness.

## Requirements

- Python 3.x
- `mss`: for capturing screen content
- `Pillow`: for processing images
- `requests`: for interacting with the Home Assistant API
- `pyyaml`: for reading the YAML configuration file
- `python-dotenv`: for loading environment variables securely

## Setup

### 1. Install Python Dependencies

Make sure you have Python 3.x installed, then install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` File

Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
HASS_URL=http://<YOUR_HOME_ASSISTANT_URL>:<PORT>
HASS_TOKEN=<HOME_ASSISTANT_ACCESS_TOKEN>
CONFIG_PATH=<PATH_TO_YOUR_CONFIG_FILE>
```

To create a token in Home Assistant, follow the instructions below.

1. Go to the [profile page](https://my.home-assistant.io/redirect/security/)
2. Click on the Security tab, then find Long-lived Access Tokens.
3. Click "Create Token"
4. Use it ;)

### 3. Create a Configuration File

Create a YAML file with the configuration for your lights. The configuration file should have the following structure:

```yaml
monitors:
  main:
    lights:
      - light_id: "light.light_1"
        screen_area: "bottom_right"
      - light_id: "light.light_2"
        screen_area: "whole_screen"

  secondary:
    lights:
      - light_id: "light.light_3"
        screen_area: "bottom_left"

number_of_updates_per_second: 10
brightness_boost: 1.5
```

- `monitors`: A dictionary where each key is the name of a monitor and the value is a list of lights that should be controlled by that monitor.

  - `lights`: A list of dictionaries where each dictionary contains the `light_id` of a light in Home Assistant and the `screen_area` that the light should be based on.
    - `light_id`: The entity ID of the light in Home Assistant.
    - `screen_area`: The area of the screen that the light should be based on. Possible values are `whole_screen`, `top_left`, `top_right`, `bottom_left`, `bottom_right`

- `number_of_updates_per_second`: The number of times per second that the screen should be captured and the lights should be updated. Lower this value if your CPU is dying.
- `brightness_boost`: A multiplier to increase the brightness of the lights.

### 4. Run the Script

Run the script using the following command:

```bash
python main.py
```

## How It Works

1. The script captures the screen content using the `mss` library.
2. The average color and brightness of the screen are calculated.
3. The script sends a request to the Home Assistant API to update the color and brightness of the lights.

## Troubleshooting

- If you encounter any issues, please open an issue on GitHub.
