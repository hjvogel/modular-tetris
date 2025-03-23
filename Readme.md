# Modular Tetris: Master Repo

## Overview

**Modular Tetris** is designed for maximum flexibility, clarity, and ease of integration, optimized for LLM-based interaction and modular plugin usage. Each component is a separate GitHub sub-repository, enabling independent management, enhancement, or replacement.

## Master Repo Structure

```
modular-tetris/
├── README.md
├── tetris-blocks-data/
├── tetris-board-engine/
├── tetris-move-controller/
├── tetris-scoring-rules/
├── tetris-game-state/
├── tetris-ui-headless/
├── tetris-play-loop/
├── tetris-ui-buttons/
├── tetris-event-bus/
├── tetris-plugin-agent/
├── tests/test_harness.py
└── examples/
    └── integration-example.json
```

## Included Modules (Sub-Repos)

1. **tetris-blocks-data**: Static definitions for Tetris blocks.
2. **tetris-board-engine**: Handles board state, collision, and piece placement.
3. **tetris-move-controller**: Processes player input into game events.
4. **tetris-scoring-rules**: Manages scoring based on gameplay.
5. **tetris-game-state**: Controls game states (start, pause, resume, end).
6. **tetris-ui-headless**: Headless interface, pluggable rendering.
7. **tetris-play-loop**: Manages game ticks and pacing.
8. **tetris-ui-buttons**: Manages UI button controls.
9. **tetris-event-bus**: Central event communication between modules.
10. **tetris-plugin-agent**: Enables LLM-based module interaction.

## Usage

### Integrating Modules

Each module provides clear JSON schemas and practical examples for immediate integration. Connect modules via the `tetris-event-bus` using standardized event types:

```json
{
  "event": "state_change",
  "state": "game_over",
  "details": {
    "reason": "collision_top",
    "final_score": 1300
  }
}
```

### Adding or Replacing Plugins

To add or replace a module:
- Create a new GitHub repo adhering to the existing JSON schema and event standards.
- Integrate it into the event bus by publishing and subscribing to standardized events.
- Replace existing modules by simply changing references in the event bus configuration.

## LLM Integration (ReplacebAI)

Use standardized LLM prompts to communicate and manage modules:

- Example prompt:
```
"Manage and synchronize game state transitions (start, pause, resume, end) based on gameplay events."
```

## Lean Development Loop

Follow this iterative process for continuous improvement:

1. **Define**: JSON schema and module purpose clearly.
2. **Develop**: Implement core functionality.
3. **Test**: Validate and refine using provided examples.
4. **Integrate**: Confirm smooth communication via the event bus.

## Contributing

Feel free to enhance or propose new modules by creating pull requests with clear documentation and schemas, following the modular approach described.

---

## integration-example.json

```json
{
  "game": {
    "state": "active",
    "score": 500,
    "level": 2,
    "current_piece": {
      "id": "T",
      "position": [4, 0],
      "rotation": 0
    },
    "next_piece": "I",
    "board": {
      "width": 10,
      "height": 20,
      "grid": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  }
}
```

---

### Next Steps:
- Continuously validate and refine integration across modules.
- Encourage community-driven enhancements and module expansions.

# Best Practice Assembly: Modular Tetris via Plugin Orchestration

## Overview

This section describes how an LLM or lightweight controller assembles all 10 modular Tetris repositories into a functional, tested, and playable Pygame-based version. It leverages the plugin-agent architecture to dynamically wire up components through JSON schemas, event publishing, and reactive handlers.

---
# Best Practice Assembly: Modular Tetris via Plugin Orchestration

## Overview

This section describes how an LLM or lightweight controller assembles all 10 modular Tetris repositories into a functional, tested, and playable Pygame-based version. It leverages the plugin-agent architecture to dynamically wire up components through JSON schemas, event publishing, and reactive handlers.

---

## Modular Assembly Process (LLM/Agent Orchestration)

### Step 1: **Plugin Registration**
The `PluginAgent` loads all modules as callable plugin handlers:

```python
agent = PluginAgent()
agent.register_module("tetris-board-engine", board_handler)
agent.register_module("tetris-move-controller", move_handler)
agent.register_module("tetris-scoring-rules", scoring_handler)
agent.register_module("tetris-game-state", state_handler)
agent.register_module("tetris-ui-buttons", button_handler)
agent.register_module("tetris-play-loop", loop_handler)
agent.register_module("tetris-event-bus", event_handler)
```

Each module implements a `handler(command, params)` interface that returns standardized JSON events.

---

### Step 2: **Initialize Event Bus**
`EventBus` is set up to allow pub-sub style messaging:

```python
bus = EventBus()
bus.subscribe("move_action", board_handler)
bus.subscribe("piece_placed", scoring_handler)
bus.subscribe("game_tick", move_handler)
bus.subscribe("button_press", state_handler)
```

This enables real-time, decoupled communication.

---

### Step 3: **UI and Play Loop Kickoff**
The `PlayLoop` begins emitting ticks. The `UIHeadless` listens for render events, and `UIButtonHandler` emits control messages.

```python
loop = PlayLoop(tick_rate=0.5)
loop.start_loop(duration_seconds=9999)
```

---

### Step 4: **Gameplay Interaction Flow**
1. User presses "Start" → UIButtons emits `button_press`
2. GameState sets `game_start` and board initializes a piece
3. `PlayLoop` ticks → `move_controller` emits a move
4. `board_engine` checks for placement → emits `piece_placed`
5. `scoring_rules` updates score
6. `UIHeadless` renders new board

Each step is driven by events and JSON payloads.

---

## LLM Runtime Command (Example)

```json
{
  "command": "rotate",
  "target_module": "tetris-move-controller",
  "parameters": {
    "piece_id": "T",
    "position": [4, 0],
    "rotation": 0
  }
}
```

The agent receives this, routes to `move_controller`, which emits a `move_action` → routed by the event bus to update the board.

---

## Testing and Observability
- Each module is tested in isolation using provided `examples/*.json`
- LLM can simulate full gameplay by emitting event chains
- Console prints or headless logs provide traceability

---

## Plugin-Based Test Harness

To run the integration harness:

```bash
python tests/test_harness.py
```

This executes commands via the `tetris-plugin-agent` interface and routes them through the modular system.

### Test Harness File: `tests/test_harness.py`

```python
import json
from ~/tetris_plugin_agent.plugin_agent import PluginAgent
from ~/tetris_event_bus.event_bus import EventBus

# Dummy handler mocks (replace with real implementations for full test)
def mock_handler(name):
    def handler(command, params):
        print(f"[{name}] Received command '{command}' with params {params}")
        return json.dumps({"status": "ok", "module": name, "command": command})
    return handler

# Register core plugins
agent = PluginAgent()
agent.register_module("tetris-board-engine", mock_handler("board"))
agent.register_module("tetris-move-controller", mock_handler("move"))
agent.register_module("tetris-scoring-rules", mock_handler("score"))
agent.register_module("tetris-game-state", mock_handler("state"))
agent.register_module("tetris-ui-buttons", mock_handler("buttons"))
agent.register_module("tetris-play-loop", mock_handler("loop"))
agent.register_module("tetris-event-bus", mock_handler("bus"))

# Sample command sequence
commands = [
    {
        "command": "start",
        "target_module": "tetris-ui-buttons",
        "parameters": {"button_id": "start"}
    },
    {
        "command": "move_left",
        "target_module": "tetris-move-controller",
        "parameters": {"piece_id": "T", "position": [4, 0], "rotation": 0}
    },
    {
        "command": "rotate",
        "target_module": "tetris-move-controller",
        "parameters": {"piece_id": "T", "position": [3, 0], "rotation": 0}
    }
]

# Execute commands
for cmd in commands:
    print("\n--- Sending Command ---")
    result = agent.handle_command(json.dumps(cmd))
    print("Response:", result)
```

---

## Final Result
This orchestrated setup enables:
- Fully playable Tetris via headless UI or Pygame
- Any component replaceable via schema-compatible plugin
- Zero hard-coded coupling between logic units
- Scalable LLM-assisted debugging and runtime control

---

## Next Steps
- Add full event routing logic across real modules
- Implement test runner with expected output assertions
- Enable agent replay/record mode for LLM-assisted debugging

