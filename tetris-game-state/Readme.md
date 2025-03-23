# Tetris Game State Repo

## Overview

This repository manages the state transitions of a modular Tetris game, providing centralized control for game start, pause, resume, and game-over scenarios. It is optimized for seamless integration with other Tetris modules and LLM-based management systems.

## Repo Structure

```
tetris-game-state/
├── README.md
├── schema.json
├── state.py
└── examples/
    ├── game-start.json
    ├── pause-resume.json
    └── game-over.json
```

## JSON Schema (`schema.json`)

Defines standardized game state transition events:

```json
{
  "event": "string",
  "state": "string",
  "details": "object"
}
```

## Example States

### Game Start (`game-start.json`)

```json
{
  "event": "state_change",
  "state": "game_start",
  "details": {
    "initial_level": 1,
    "initial_score": 0
  }
}
```

### Pause and Resume (`pause-resume.json`)

```json
{
  "event": "state_change",
  "state": "paused",
  "details": {
    "paused_at": "2025-04-01T12:00:00Z"
  }
}
```

### Game Over (`game-over.json`)

```json
{
  "event": "state_change",
  "state": "game_over",
  "details": {
    "reason": "collision_top",
    "final_score": 1350,
    "level_reached": 4
  }
}
```

## Usage & Integration

Send and receive standardized JSON events to maintain and synchronize game states across your Tetris module network.

### Example LLM Integration Prompt (ReplacebAI)

```
"Synchronize and control Tetris game state transitions including start, pause, resume, and game over."
```

## state.py

```python
import json
from datetime import datetime

class GameState:
    def __init__(self):
        self.state = "initialized"
        self.details = {}

    def set_state(self, state, details=None):
        self.state = state
        self.details = details or {}
        event = {
            "event": "state_change",
            "state": self.state,
            "details": self.details
        }
        return json.dumps(event)

    def game_start(self, initial_level=1, initial_score=0):
        return self.set_state("game_start", {
            "initial_level": initial_level,
            "initial_score": initial_score
        })

    def pause_game(self):
        return self.set_state("paused", {
            "paused_at": datetime.utcnow().isoformat() + "Z"
        })

    def resume_game(self):
        return self.set_state("resumed", {
            "resumed_at": datetime.utcnow().isoformat() + "Z"
        })

    def game_over(self, reason, final_score, level_reached):
        return self.set_state("game_over", {
            "reason": reason,
            "final_score": final_score,
            "level_reached": level_reached
        })

# Example usage with pygame (pseudo-integration)
# game_state = GameState()
# print(game_state.game_start())
# print(game_state.pause_game())
# print(game_state.resume_game())
# print(game_state.game_over("collision_top", 1350, 4))
```

## Lean Development Loop

1. **Define** clear and concise JSON schemas for states.
2. **Develop** complete state transition examples.
3. **Test** state integrity and seamless transition handling.
4. **Integrate** thoroughly with other Tetris modules and plugins.

---

## Next Steps
- Continuously refine based on integration testing and user feedback.
- Expand documentation and state transition examples for enhanced clarity.

