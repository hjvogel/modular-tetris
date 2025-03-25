import json
import time

class UIButtonHandler:
    def __init__(self):
        pass

    def button_pressed(self, button_id):
        event = {
            "event": "button_press",
            "source": "tetris-ui-buttons",
            "button_id": button_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        return json.dumps(event)

button_handler = UIButtonHandler()

def handler(command, params):
    if command == "button_press":
        return button_handler.button_pressed(params.get("button_id", "unknown"))
    return json.dumps({
        "error": "Unknown button command",
        "received": command
    })