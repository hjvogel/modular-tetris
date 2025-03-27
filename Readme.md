# Modular Tetris: Master Repo

## Overview

**Modular Tetris** is a highly pluggable, fully decoupled, LLM-friendly architecture that implements Tetris using reusable, independently testable **modules**. Every component of gameplay—board, movement, UI, scoring, game logic—is built as its **own micro-repository** and **communicates only through JSON**.

> ✅ **No hardcoded game logic in `main.py`**  
> ✅ **Pluggable UI, logic, rendering, and control layers**  
> ✅ **Ready for AI orchestration, plugin economics, and NFT-like tokenized code**

---

## Repo Structure

```
modular-tetris/
├── main.py
├── plugin_agent.py
├── event_bus.py
├── play_loop.py
├── ui_headless.py
├── tetris-blocks-data/
├── tetris-board-engine/
│   └── tetris_ui_config.json
├── tetris-move-controller/
├── tetris-scoring-rules/
├── tetris-game-state/
├── tetris-ui-buttons/
├── examples/
│   ├── integration-example.json
│   ├── plugin-command.json
│   ├── render-board.json
│   ├── tick-event.json
│   ├── ui-event.json
│   └── sample-event.json
├── tests/
│   └── test_harness.py
└── README.md
```

---

## Included Modules

| Module                   | Purpose                                                  |
|--------------------------|----------------------------------------------------------|
| `tetris-blocks-data`     | JSON-only piece definitions                              |
| `tetris-board-engine`    | Board state, collision, placement                        |
| `tetris-move-controller` | Movement interpretation, position calculation            |
| `tetris-scoring-rules`   | Score logic and line-clear detection                     |
| `tetris-game-state`      | Tracks gameplay state (start, pause, resume, end)        |
| `tetris-ui-buttons`      | Button rendering + events                                |
| `ui-headless`            | Pygame canvas rendering (no layout logic hardcoded)      |
| `play_loop.py`           | Emits ticks as timed JSON events                         |

---

## Core Infrastructure

| Component         | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `plugin_agent.py` | Registers modules and dispatches structured JSON commands                 |
| `event_bus.py`    | Manages pub-sub event routing between modules using `event_type` channels |
| `ui_headless.py`  | Headless UI rendering with JSON-driven layout from `tetris_ui_config.json`|

---

## Run the Game

```bash
python main.py
```

Then click **Start** or use the arrow keys (⬅️➡️⬇️⬆️) to play.

---

## JSON API Communication

Every interaction is JSON-driven:

### Event Bus Payload Example

```json
{
  "event": "score_update",
  "source": "tetris-scoring-rules",
  "payload": { "total_score": 1000 },
  "timestamp": "2025-04-01T12:00:05Z"
}
```

### Plugin Agent Command Example

```json
{
  "command": "move_left",
  "target_module": "tetris-move-controller",
  "parameters": { "position": [4, 0] }
}
```

---

## Modular Assembly Flow (LLM Orchestrated)

### Step 1: Register Plugins

```python
agent.register_module("tetris-board-engine", board.handler)
agent.register_module("tetris-move-controller", move.handler)
agent.register_module("tetris-scoring-rules", scoring.handler)
agent.register_module("tetris-game-state", state.handler)
agent.register_module("tetris-ui-buttons", buttons.handler)

agent.register_module("play-loop", play_loop.handler)
agent.register_module("ui-headless", ui.handler)
```

### Step 2: Setup Event Routing

```python
bus.subscribe("button_press", state.handler)
bus.subscribe("state_change", board.handler)
bus.subscribe("move_action", board.handler)
bus.subscribe("piece_placed", scoring.handler)
bus.subscribe("score_update", ui.handler)
```

### Step 3: Game Loop & Tick Events

```python
def loop_runner():
    for _ in range(999):
        tick = json.loads(agent.handle_command(json.dumps({
            "command": "create_tick",
            "target_module": "play-loop"
        })))
        bus.publish("game_tick", "play-loop", tick)
        time.sleep(1)
```

---

## Test Harness

```python
from plugin_agent import PluginAgent
agent = PluginAgent()
agent.register_module("tetris-ui-buttons", mock_handler("buttons"))
agent.register_module("tetris-move-controller", mock_handler("move"))
```

Run tests using:
```bash
python tests/test_harness.py
```

---

## Tokenization Vision: The Future of Modular Games

This project lays the foundation for **economic plugin ecosystems**.

- Every module is independently swappable - improvable - open for best of breed.
- Each plugin could be tokenized like an image, NFT, or microservice once value is slightly above 0.
- Ownership of a `tetris-*` or just a `game-*` repo can represent value: contribute better game-logics, claim micro-rewards.
- Use LLMs to benchmark plugin performance, reliability, or innovation.

> Imagine a world where creating a better scoring system earns you real-time micro-payments in open game economies.  
> This is **open protocol gaming**—backed by JSON, extensible by LLMs, and driven by incentives.

---

## LLM Prompt Examples (ReplacebAI)

```
"Send a command to pause the game."
"Request a tick event from the loop module."
"Query the current board state and score."
```

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

## Why This Matters

- **LLM-Safe**: Every action can be represented in plain JSON.
- **Game Agnostic**: Swap Tetris logic for Chess or Snake without code rewrite.
- **Extensible**: Just add a module folder and register it.
- **Tokenizable**: The first open framework for NFT-like **modular game logic**.

---

## Roadmap

- [ ] Add scoring plugin market (token economics)
- [ ] Publish event schemas as open standard
- [ ] Train LLM agents to improve performance and UX
- [ ] Enable browser-based headless rendering + WebSocket bridge

---

## Join the Movement

Build smarter games  
Refactor with intent  
Earn from improvements - Tokenized Code Economy incoming
Plug into the **Composable Gaming Economy**