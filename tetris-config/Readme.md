# Tetris Config Module (`tetris-config`)

This module contains the **master configuration** for the Tetris game within the **Modular Tetris** ecosystem. It provides all essential settings and module paths, enabling flexible, decoupled game integration, easy plugin management, and straightforward extension or customization.

---

## Folder Structure

```
tetris-config/
├── README.md
└── game_config.json
```

---

## Purpose

The `game_config.json` acts as a centralized configuration specifying:

- **Game Metadata**: Name, description, licensing, and payment rules.
- **Module Registration**: Modules used in gameplay (board, movement, scoring, etc.).
- **Event Subscriptions**: Event-driven wiring for module interactions.
- **UI Configuration**: UI parameters such as colors, layout, cell sizes, and labels.
- **Gameplay Control**: Game tick rates, commands, and game logic rules.

This structure supports easy module swapping, rapid prototyping, and LLM-driven orchestration.

---

## Example Configuration (`game_config.json`)

```json
{
  "game_id": "tetris",
  "game_name": "Modular Tetris",
  "description": "A modular, JSON-driven implementation of Tetris for microservices testing, plugin economics, and LLM integration.",
  "intention": "Demonstrate tokenized game logic modules, enabling remixable game architectures.",
  "license": "MIT",
  "micro_payments": {
    "start_game": 0.001,
    "line_clear": 0.0005,
    "rotate_piece": 0.0001
  },
  "modules": [
    {"name": "board-engine", "import_name": "board"},
    {"name": "move-controller", "import_name": "move"},
    {"name": "scoring-rules", "import_name": "scoring"},
    {"name": "game-state", "import_name": "state"},
    {"name": "ui-buttons", "import_name": "buttons"},
    {"name": "ui-headless", "import_name": "ui_headless"},
    {"name": "play-loop", "import_name": "play_loop"}
  ],
  "plugin_paths": [
    "./tetris-board-engine",
    "./tetris-move-controller",
    "./tetris-scoring-rules",
    "./tetris-game-state",
    "./tetris-ui-buttons"
  ],
  "event_subscriptions": [
    {"event_type": "button_press", "target_module": "game-state"},
    {"event_type": "state_change", "target_module": "board-engine"},
    {"event_type": "move_action", "target_module": "board-engine"},
    {"event_type": "piece_placed", "target_module": "scoring-rules"},
    {"event_type": "score_update", "target_module": "ui-headless"},
    {"event_type": "game_tick", "target_module": "game-state"}
  ],
  "key_events": {
    "1073741904": "move_left",
    "1073741903": "move_right",
    "1073741905": "move_down",
    "1073741906": "rotate"
  },
  "button_actions": {
    "start": "start",
    "pause": "pause",
    "quit": "quit"
  },
  "state_module": "game-state",
  "scoring_module": "scoring-rules",
  "board_module": "board-engine",
  "board_get_command": "get_board",
  "score_get_command": "get_score",
  "loop_module": "play-loop",
  "tick_create_command": "create_tick",
  "tick_count": 9999,
  "tick_interval": 1,
  "ui_config": {
    "cell_size": 30,
    "grid_width": 10,
    "grid_height": 20,
    "button_height": 40,
    "font": "Arial",
    "font_size": 20,
    "bg_color": [0, 0, 0],
    "score_label": "Score",
    "buttons": [
      {"id": "start", "label": "Start", "pos": [10, 605]},
      {"id": "pause", "label": "Pause", "pos": [110, 605]},
      {"id": "quit", "label": "Quit", "pos": [210, 605]}
    ],
    "colors": {
      "0": [0, 0, 0],
      "default": [200, 200, 200]
    }
  }
}
```

---

## How to Add a New Game

To integrate a completely new modular game (e.g., **Snake**, **Chess**, etc.):

### Step 1: Create a New Game Config

- Create a new folder under the master repo (e.g., `snake-config`) or just create a new own game specific repo and connect it to the master here.
- Copy and customize the `game_config.json` with your new game settings:

```json
{
  "game_id": "snake",
  "game_name": "Modular Snake",
  "...": "...",
  "modules": [
    {"name": "snake-board", "import_name": "snake_board"},
    {"name": "snake-move", "import_name": "snake_move"},
    {"name": "snake-score", "import_name": "snake_scoring"}
  ],
  "plugin_paths": [
    "./snake-board",
    "./snake-move-controller",
    "./snake-scoring-rules"
  ],
  "event_subscriptions": [
    {"event_type": "move_event", "target_module": "snake-board"},
    {"event_type": "score_event", "target_module": "snake-scoring"}
  ],
  "...": "..."
}
```

---

### Step 2: Develop or Fork New Modules

- Create repositories or folders for each new game module (`snake-board`, `snake-move-controller`, etc.).
- Ensure each implements a standardized plugin handler (`handler(command, params)`).

Example module structure:

```
snake-board/
├── board.py
├── schema.json
└── examples/
    └── sample-event.json
```

---

### Step 3: Integrate into Main

In your master `main.py`:

- Point to the new game configuration:
```python
CONFIG_PATH = "./snake-config/game_config.json"
```

- Run the game to test module integration:
```bash
python main.py
```

---

## Lean Development Loop for New Games

Follow these steps to rapidly iterate on new game integrations:

1. **Define clear schemas** for JSON commands/events.
2. **Develop isolated game modules** using standardized handlers.
3. **Test modules individually** with unit tests (`tests/test_harness.py`).
4. **Integrate modules via `plugin_agent.py` and `event_bus.py`**.
5. **Verify game functionality** end-to-end using the master configuration.

---

## Best Practices for Extending the Modular Ecosystem

- **Clearly document your module's JSON schemas** for easier integration.
- **Adhere to established event naming conventions** (`game_tick`, `score_update`, etc.).
- **Minimize coupling** by ensuring modules never directly interact outside structured JSON events.
- **Validate modules independently** before integrating into the master game.

---

## Next Steps & Roadmap for Config Module

- [ ] Implement dynamic multi-game switching in `main.py`
- [ ] Expand the modular marketplace for plugin economics
- [ ] Publish open schema standards for community interoperability
- [ ] Automate LLM-assisted code validation and quality checks

---

## Join the Modular Game-Building Community

Help us build a smarter, more open gaming ecosystem—driven by clear incentives, tokenized modules, and easy composability.

**Start building. Start earning. Start modular.**