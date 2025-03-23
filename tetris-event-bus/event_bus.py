import json
import time

class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type, source, payload):
        event = {
            "event": event_type,
            "source": source,
            "payload": payload,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        event_json = json.dumps(event)
        for callback in self.subscribers.get(event_type, []):
            callback(event_json)

# Example usage with pseudo-integration
# def handle_event(event_json):
#     print("Received event:", event_json)
# 
# bus = EventBus()
# bus.subscribe("piece_placed", handle_event)
# bus.publish("piece_placed", "tetris-board-engine", {"piece_id": "T", "position": [4, 1], "rotation": 90})