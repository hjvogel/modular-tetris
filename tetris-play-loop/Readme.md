# Tetris Play Loop Repo

## Overview

This repository manages the core game loop for Tetris, handling timing, game ticks, and pacing. Designed to integrate seamlessly with other Tetris modules and front-end implementations, it optimizes gameplay consistency and responsiveness.

## Repo Structure

```
tetris-play-loop/
├── README.md
├── schema.json
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
```

## Lean Development Loop

1. **Define** clear JSON schema for tick events.
2. **Develop** efficient timing and tick logic.
3. **Test** gameplay synchronization and event consistency.
4. **Integrate** smoothly with board, UI, and control modules.

---

## Next Steps
- Continuously refine timing and responsiveness based on feedback.
- Expand loop management documentation and examples.

