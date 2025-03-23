# Tetris Event Bus Repo

## Overview

This repository provides a central communication hub for modular Tetris gameplay, managing event distribution among modules like gameplay logic, UI components, and scoring. It ensures synchronized, efficient, and consistent inter-module communication through standardized events.

## Repo Structure

```
tetris-event-bus/
├── README.md
├── schema.json
├── event_bus.py
└── examples/
    └── sample-event.json
```

## JSON Schema (`schema.json`)

Defines the standardized event structure for communication:

```json
{
  "event": "string",
  "source": "string",
  "payload": "object",
  "timestamp": "string"
}
```

## Example Event (`sample-event.json`)

```json
{
  "event": "piece_placed",
  "source": "tetris-board-engine",
  "payload": {
    "piece_id": "T",
    "position": [4, 1],
    "rotation": 90
  },
  "timestamp": "2025-04-01T12:00:05Z"
}
```

## Usage & Integration

Use the event bus to publish and subscribe to standardized JSON events, ensuring modules remain synchronized and responsive.

### Example LLM Integration Prompt (ReplacebAI)

```
"Facilitate standardized event communication and synchronization across Tetris modules."
```

## event_bus.py

```python
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
```

## Lean Development Loop

1. **Define** standardized JSON schema for events.
2. **Develop** robust publish-subscribe logic.
3. **Test** event broadcasting and subscription responsiveness.
4. **Integrate** seamlessly with other Tetris modules.

---

## Next Steps
- Continuously refine event management based on module feedback.
- Expand documentation and practical usage examples.

