# Modular Tetris: Master Repo

## Overview

**Modular Tetris** is a highly pluggable, fully decoupled, LLM-friendly architecture implementing Tetris with reusable, independently testable **modules**. Every aspect of gameplay—board, movement, UI, scoring, and game logic—is maintained as its own micro-repository and communicates exclusively via structured JSON events.

> ✅ **No hardcoded logic in `main.py`**  
> ✅ **Flexible UI, logic, rendering, and controls**  
> ✅ **AI-ready orchestration and NFT-like tokenization**

---

## Updated Repo Structure

```
modular-tetris/
├── main.py
├── plugin_agent.py
├── event_bus.py
├── play_loop.py
├── ui_headless.py
├── tetris-config/
│   └── game_config.json
├── tetris-blocks-data/
├── tetris-board-engine/
│   └── board.py
├── tetris-move-controller/
│   └── move.py
├── tetris-scoring-rules/
│   └── scoring.py
├── tetris-game-state/
│   └── state.py
├── tetris-ui-buttons/
│   └── buttons.py
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
| `tetris-blocks-data`     | JSON-defined Tetris blocks with rotations and colors     |
| `tetris-board-engine`    | Grid management, collision detection, line clearing      |
| `tetris-move-controller` | User input interpretation and position updates           |
| `tetris-scoring-rules`   | Score tracking based on lines cleared                    |
| `tetris-game-state`      | Gameplay states: start, pause, resume, game over         |
| `tetris-ui-buttons`      | UI button events handling                                |
| `ui_headless.py`         | Flexible Pygame rendering (JSON-configurable layout)     |
| `play_loop.py`           | Periodic game tick emitter                               |

---

## Core Infrastructure

| Component         | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `plugin_agent.py` | Dynamic module registration and JSON command dispatching                  |
| `event_bus.py`    | Pub/sub JSON event handling between independent modules                   |
| `ui_headless.py`  | JSON-driven headless UI renderer, extensible for any game                 |

---

## Running the Modular Game

```bash
python main.py
```

Click **Start** to play or use arrow keys (⬅️➡️⬇️⬆️).

---

## JSON Event Communication

Modules interact strictly through JSON events:

### Event Bus Example

```json
{
  "event": "score_update",
  "source": "tetris-scoring-rules",
  "payload": { "total_score": 1000 },
  "timestamp": "2025-04-01T12:00:05Z"
}
```

### Plugin Agent Example Command

```json
{
  "command": "rotate",
  "target_module": "tetris-move-controller",
  "parameters": { "position": [5, 1] }
}
```

---

## Modular Integration Flow

### Step 1: Registering Plugins (from `game_config.json`)

Plugins are registered dynamically from the config:

```python
for module in config["modules"]:
    agent.register_module(module["name"], plugins[module["name"]].handler)
```

### Step 2: Event Bus Setup (configurable)

Event subscriptions from JSON config:

```python
for sub in config["event_subscriptions"]:
    bus.subscribe(sub["event_type"], plugins[sub["target_module"]].handler)
```

### Step 3: Game Loop Execution (generic)

```python
def loop_runner():
    for _ in range(config["tick_count"]):
        tick = json.loads(agent.handle_command(json.dumps({
            "command": config["tick_create_command"],
            "target_module": config["loop_module"]
        })))
        bus.publish("game_tick", config["loop_module"], tick)
        time.sleep(config["tick_interval"])
```

---

## Extensible Test Harness

Quickly validate module communication:

```bash
python tests/test_harness.py
```

---

## Tokenization and Modular Economics Vision

**Modular Tetris** is a foundational step toward a broader **tokenized code marketplace**:

- Each module (`tetris-board-engine`, `tetris-scoring-rules`) could be tokenized and economically incentivized.
- Contributors earn micropayments based on the quality, efficiency, and popularity of their modules.
- LLM-assisted benchmarking to fairly assess plugin performance and value.

> Imagine building and earning from an open, composable marketplace for game components. This modular architecture lays the groundwork.

---

## LLM Integration Prompts (ReplacebAI)

Example AI integration prompts:

```
"Send JSON command to start a new game."
"Request current score from the scoring module."
"Rotate current block clockwise using move controller."
```

---

## Example Integration JSON (`integration-example.json`)

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
      "grid": [[0,0,0,0,0,0,0,0,0,0]] * 20
    }
  }
}
```

---

## Why Modular?

- **LLM-safe**: JSON-only interactions, easily parsed by AI.
- **Game Agnostic**: Quickly adapt to other games or scenarios without major rewrites.
- **Composable**: Easily swap components, improve logic, rendering or scoring.
- **Tokenizable**: Enable genuine economic incentives and code ownership.

---

## Project Roadmap & Next Steps

- [x] Generalized configuration (`game_config.json`) for easy game swapping
- [ ] Integrated multi-game selector in `main.py` (Chess, Snake, etc.)
- [ ] Launch an open plugin marketplace for code economy
- [ ] Publish event schemas as an open interoperability standard
- [ ] Implement browser-based headless rendering (WebSocket)
- [ ] LLM-powered plugin analysis and scoring mechanisms

---

## Future Expansion: Adding Other Games

1. **Create a new config JSON** for the desired game (e.g., Snake, Chess).
2. **Implement or fork necessary plugin repos** matching the modular schema.
3. **Add new modules** to `plugin_paths` and `modules` in the game config.
4. **Run main.py** and select new game via integrated selector.

---

## How to Contribute

- **Fork** individual modules (`tetris-board-engine`, etc.) and improve.
- **Extend** or create new modules following JSON-schema guidelines.
- **Integrate** your plugin through pull requests and community feedback.

---

## Join the Movement

Help build a new era of modular, composable games:  

✅ **Refactor** with clear incentives  
✅ **Contribute** to openly tokenizable modules or sub modules  
✅ **Earn rewards** from code improvements or just gameing  

Plug into the **Open Composable Game-Building Economy** today!