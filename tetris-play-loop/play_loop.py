import json
import time

class PlayLoop:
    def __init__(self, tick_rate=1):
        self.tick_rate = tick_rate
        self.tick_number = 0

    def start_loop(self, duration_seconds=60):
        start_time = time.time()
        while (time.time() - start_time) < duration_seconds:
            self.tick_number += 1
            event = self.create_tick_event()
            print(event)
            time.sleep(self.tick_rate)

    def create_tick_event(self):
        event = {
            "event": "game_tick",
            "tick_number": self.tick_number,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        return json.dumps(event)

# Example usage with pygame (pseudo-integration)
# loop = PlayLoop(tick_rate=0.5)
# loop.start_loop(duration_seconds=30)