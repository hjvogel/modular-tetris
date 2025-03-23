import json
import time

class UIButtonHandler:
    def __init__(self):
        pass

    def button_pressed(self, button_id):
        event = {
            "event": "button_press",
            "button_id": button_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        return json.dumps(event)

# Example usage with pygame (pseudo-integration)
# button_handler = UIButtonHandler()
# print(button_handler.button_pressed("start"))
# print(button_handler.button_pressed("pause"))