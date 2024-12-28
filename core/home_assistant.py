import requests

class HomeAssistant:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def change_color(self, light_id, color, brightness, transition=0.2):
        """
        Change the color and brightness of a light in Home Assistant with a smooth transition.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "entity_id": light_id,
            "rgb_color": list(map(int, color)),
            "brightness": int(brightness),
            "transition": transition,
        }

        try:
            response = requests.post(
                f"{self.url}/api/services/light/turn_on",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
