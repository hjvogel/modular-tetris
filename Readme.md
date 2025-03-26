
# Modular Tetris: Master Repo

## Overview

**Modular Tetris** is a highly pluggable, fully decoupled, LLM-friendly implementation here of Tetris or any other game where every game component is its own independent module. All modules communicate strictly through JSON commands and events, orchestrated by a lightweight `plugin_agent.py` and routed by `event_bus.py`.

This architecture supports dynamic plugin registration, low-code extensibility, and easy interaction with LLMs, GUI-less runtimes, or web-based UIs.

---

## Repo Structure

```
modular-tetris/
├── main.py
├── plugin_agent.py
├── event_bus.py
├── examples/
│   ├── integration-example.json
│   ├── plugin-command.json
│   └── sample-event.json
├── tetris-blocks-data/
├── tetris-board-engine/
├── tetris-move-controller/
├── tetris-scoring-rules/
├── tetris-game-state/
├── tetris-ui-headless/
├── tetris-play-loop/
├── tetris-ui-buttons/
├── tests/
│   └── test_harness.py
└── README(s).md
```

---

## Included Modules

Each sub-repo is imported as a Python plugin and implements a JSON-compatible handler:

| Module                    | Purpose                                             |
|--------------------------|-----------------------------------------------------|
| `tetris-blocks-data`     | Static JSON definitions for all Tetris block shapes |
| `tetris-board-engine`    | Grid, placement, and collision detection            |
| `tetris-move-controller` | Interprets user input into movement events          |
| `tetris-scoring-rules`   | Calculates score based on lines cleared             |
| `tetris-game-state`      | Handles gameplay lifecycle events                   |
| `tetris-ui-headless`     | Renders the board using Pygame or headless console  |
| `tetris-play-loop`       | Emits periodic game tick events                     |
| `tetris-ui-buttons`      | Handles UI button click events                      |

---

## Core Infrastructure

| Component        | Description |
|------------------|-------------|
| `plugin_agent.py` | Registers callable plugins and routes commands by target module |
| `event_bus.py`    | Enables pub-sub message flow between modules using JSON events  |

---

## Usage

### Launch the Game

```bash
python main.py
```

### Start Game (via UI)

Click the `Start` button to begin gameplay. Use arrow keys to control blocks.

---

## Event Bus Communication

All modules use the `EventBus` to send or receive structured events:

```json
{
  "event": "score_update",
  "source": "tetris-scoring-rules",
  "payload": {
    "total_score": 800
  },
  "timestamp": "2025-04-01T12:00:05Z"
}
```

---

## Plugin Agent Command Routing

Example JSON command that gets routed via `plugin_agent.py`:

```json
{
  "command": "move_left",
  "target_module": "piece-move-controller",
  "parameters": {
    "position": [4, 0]
  }
}
```

---

## LLM Integration Example (ReplacebAI)

```
"Rotate the active Tetris piece clockwise by sending a 'rotate' command to the move controller."
```

---

## Best Practice Assembly: Modular Tetris via Plugin Orchestration

This is how `main.py` glues everything together:

### Step 1: Register Plugins

```python
agent = PluginAgent()
agent.register_module("tetris-board-engine", board.handler)
agent.register_module("tetris-move-controller", move.handler)
agent.register_module("tetris-scoring-rules", scoring.handler)
agent.register_module("tetris-game-state", state.handler)
agent.register_module("tetris-ui-buttons", buttons.handler)
agent.register_module("tetris-play-loop", play_loop.handler)
agent.register_module("tetris-ui-headless", ui.handler)
```

---

### Step 2: Setup Event Bus

```python
bus = EventBus()
bus.subscribe("button_press", state.handler)
bus.subscribe("state_change", board.handler)
bus.subscribe("move_action", board.handler)
bus.subscribe("piece_placed", scoring.handler)
bus.subscribe("score_update", ui.handler)
```

---

### Step 3: Run Tick Loop

The game loop emits tick events that move the piece down periodically.

```python
def loop_runner():
    for _ in range(999):
        tick = json.loads(agent.handle_command(json.dumps({
            "command": "create_tick",
            "target_module": "tetris-play-loop"
        })))
        bus.publish("game_tick", "tetris-play-loop", tick)
        time.sleep(1)
```

---

## Test Harness (`tests/test_harness.py`)

A mock test file to validate plugin commands without full GUI or engine:

```python
from plugin_agent import PluginAgent
from event_bus import EventBus

agent = PluginAgent()
bus = EventBus()

def mock_handler(name):
    def handler(command, params):
        print(f"[{name}] Received '{command}' with params {params}")
        return json.dumps({"status": "ok"})
    return handler

agent.register_module("tetris-move-controller", mock_handler("move"))
agent.register_module("tetris-ui-buttons", mock_handler("buttons"))

commands = [
    {"command": "start", "target_module": "tetris-ui-buttons", "parameters": {}},
    {"command": "move_left", "target_module": "tetris-move-controller", "parameters": {"position": [0, 0]}}
]

for cmd in commands:
    print(agent.handle_command(json.dumps(cmd)))
```

---

## Lean Development Loop

1. **Define**: JSON schema for command and event interfaces.
2. **Develop**: Module as a plugin with `handler(command, params)` function.
3. **Test**: Use the harness or manual plugin registration.
4. **Integrate**: Hook into the bus, use the agent, render via UI module.

---

## Contributing

- Fork any module and make improvements
- New modules must respect the plugin interface and schemas
- Submit integration example and sample test in `examples/`

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
      "grid": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] * 20
    }
  }
}
```

---

## Why Is It Modular?

- **No hardcoded game rules** in `main.py`
- All pieces are plugins: board, move, scoring, state
- Easy to swap rendering system, add AI, etc.
- LLM or CLI can command the system via JSON

---

## Next Steps

- Add more UIs (WebSocket, Tkinter, browser)
- Extend test coverage across plugin boundaries
- Train LLM agents to control gameplay using schema and event logs