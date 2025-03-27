# Tetris Play Loop Repo

## Overview

This repository manages the core game loop for Tetris, handling timing, game ticks, and pacing. Designed to integrate seamlessly with other Tetris modules and front-end implementations, it optimizes gameplay consistency and responsiveness.

## Repo Structure

```
root
├── README.md
├── (schema.json)
├── play_loop.py
└── examples/
    └── tick-event.json
```

## JSON Schema (`schema.json`)

Defines the structure for gameplay tick events:

```json
{
  "event": "string",
  "tick_number": "integer",
  "timestamp": "string"
}
```

## Example Gameplay Tick (`tick-event.json`)

```json
{
  "event": "game_tick",
  "tick_number": 150,
  "timestamp": "2025-04-01T12:00:05Z"
}
```

## Usage & Integration

Use standardized tick events to synchronize the Tetris gameplay pacing with other modules like the board engine, move controller, and UI elements.

### Example LLM Integration Prompt (ReplacebAI)

```
"Manage game ticks and synchronize gameplay events consistently."
```

## play_loop.py

```python
mport json
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
            "source": "play-loop",
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
```

## Headless / Test Mode Support

Although the `start_loop()` method is not used by the interactive Pygame UI mode, it is intentionally kept in the codebase for:

- **Automated simulation or test runs**
- **Headless gameplay scenarios (e.g., LLM testing, CI/CD pipelines)**
- **Future modes (demo playback, benchmarking, scripting)**

This supports better separation of UI and logic, and enables broader plugin reuse beyond the Pygame interface.

## Lean Development Loop

1. **Define** clear JSON schema for tick events.
2. **Develop** efficient timing and tick logic.
3. **Test** gameplay synchronization and event consistency.
4. **Integrate** smoothly with board, UI, and control modules.

---

## Next Steps
- Continuously refine timing and responsiveness based on feedback.
- Expand loop management documentation and examples.
