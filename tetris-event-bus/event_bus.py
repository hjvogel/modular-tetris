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

        for callback in self.subscribers.get(event_type, []):
            try:
                callback(event_type, payload)
            except Exception as e:
                print(f"[EventBus Error] Failed to call subscriber for {event_type}: {e}")


# Example usage
# def handle_event(command, params):
#     print("Handled:", command, params)
#
# bus = EventBus()
# bus.subscribe("state_change", handle_event)
# bus.publish("state_change", "tetris-game-state", {"state": "start"})