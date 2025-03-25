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
            "source": "tetris-play-loop",
            "tick_number": self.tick_number,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        return json.dumps(event)

# Singleton instance
loop = PlayLoop()

# Plugin-compatible handler
def handler(command, params):
    if command == "create_tick":
        return loop.create_tick_event()
    elif command == "start_loop":
        duration = params.get("duration_seconds", 10)
        loop.start_loop(duration)
        return json.dumps({"status": "loop_complete"})
    return json.dumps({
        "error": "Unknown loop command",
        "received": command
    })
