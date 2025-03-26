
# Modular Event Bus Repo

## Overview

This repository provides a lightweight, pluggable event bus system for modular applications. It facilitates standardized communication between decoupled modules using a publish-subscribe architecture with structured JSON events.

Ideal for use in games, automation pipelines, simulation engines, plugin frameworks, or any event-driven system.

## Repo Structure

```
modular-event-bus/
├── README.md
├── schema.json
├── event_bus.py
└── examples/
    └── sample-event.json
```

## JSON Schema (`schema.json`)

Defines the structure for all events passed between modules:

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
  "event": "entity_updated",
  "source": "ai-agent-manager",
  "payload": {
    "entity_id": "agent_42",
    "status": "moving",
    "position": [10, 5]
  },
  "timestamp": "2025-04-01T12:00:05Z"
}
```

## Usage & Integration

Use this bus to publish and subscribe to structured events between system modules.

- Each `event` is published with a `type`, `source`, `payload`, and timestamp.
- Any number of subscribers can listen to a specific event type.

### Example LLM Integration Prompt

```
"Facilitate structured event communication between modular subsystems via a plugin-compatible event bus."
```

## `event_bus.py`

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

        for callback in self.subscribers.get(event_type, []):
            try:
                callback(event_type, payload)
            except Exception as e:
                print(f"[EventBus Error] Failed to call subscriber for {event_type}: {e}")
```

## Example Usage

```python
def handle_entity_update(event_type, payload):
    print(f"[Handler] {event_type} received:", payload)

bus = EventBus()
bus.subscribe("entity_updated", handle_entity_update)

bus.publish("entity_updated", "sim-engine", {
    "entity_id": "npc_001",
    "position": [7, 2],
    "velocity": [0, -1]
})
```

## Lean Development Loop

1. **Define** standardized schema for your events.
2. **Implement** lightweight event bus to handle subscriptions.
3. **Connect** modular systems through event publishing.
4. **Test** system responsiveness, chaining, and decoupling.

---

## Next Steps

- Add event logging or replay features.
- Support async or networked dispatching.
- Expand schema validation (e.g., with `jsonschema`).