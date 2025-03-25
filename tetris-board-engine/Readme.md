# Tetris Board Engine Repo

## Overview

This repository handles board state management, collision detection, and piece placement for a modular Tetris game, clearly structured for integration with other Tetris modules and optimized for easy interaction with LLM-based plugins.

## Repo Structure

```
tetris-board-engine/
├── README.md
├── schema.json
├── board.py
├── move.py
└── examples/
    ├── empty-board.json
    └── example-move.json
```

## JSON Schema (`schema.json`)

Defines the structure for board states and move events:

```json
{
  "width": "integer",
  "height": "integer",
  "grid": "array"
}
```

## Example Board States

### Empty Board (`empty-board.json`)

```json
{
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
```

### Example Move (`example-move.json`)

```json
{
  "piece_id": "T",
  "position": [4, 0],
  "rotation": 0
}
```

## Usage & Integration

Receive move events, manage the board state, handle collision detection, and send board updates to other modules.

### Example LLM Integration Prompt (ReplacebAI)

```
"Update Tetris board state based on piece placement and detect collisions."
```

## board.py

```python
import json

class TetrisBoard:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def is_collision(self, piece_shape, position):
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    gx, gy = px + x, py + y
                    if gx < 0 or gx >= self.width or gy >= self.height:
                        return True
                    if gy >= 0 and self.grid[gy][gx]:
                        return True
        return False

    def place_piece(self, piece_shape, position, color=(255, 0, 255)):
        if self.is_collision(piece_shape, position):
            return False
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    gx, gy = px + x, py + y
                    if 0 <= gx < self.width and 0 <= gy < self.height:
                        self.grid[gy][gx] = color
        return True

    def get_board_state(self):
        return {
            "width": self.width,
            "height": self.height,
            "grid": self.grid
        }

board = TetrisBoard()

def handler(command, params):
    if command == "place_piece":
        shape = params.get("shape")
        position = params.get("position")
        color = params.get("color", "#FF00FF")
        if isinstance(color, str) and color.startswith("#"):
            color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        success = board.place_piece(shape, position, color)
        return json.dumps({"placed": success, "grid": board.grid})

    elif command == "get_board":
        return json.dumps(board.get_board_state())

    return json.dumps({"error": "Unknown board command", "received": command})
```

move.py
```
# move.py
import json

# Directional offsets
OFFSETS = {
    "left": (-1, 0),
    "right": (1, 0),
    "down": (0, 1),
    "rotate": (0, 0)
}

# This function simulates movement; actual shape is managed by board engine
def handler(command, params):
    if command in ["move_left", "move_right", "move_down", "rotate", "drop"]:
        move_type = command.split("_")[-1] if "_" in command else command

        event = {
            "event": "move_action",
            "source": "tetris-move-controller",
            "payload": {
                "move": move_type,
                "offset": OFFSETS.get(move_type, (0, 1)),
                "rotate": (move_type == "rotate"),
                "drop": (move_type == "drop")
            }
        }
        return json.dumps(event)

    return json.dumps({
        "error": "Unknown move command",
        "received": command
    })
```

## Lean Development Loop

1. **Define** clear board state and move event schemas.
2. **Develop** robust collision detection and placement logic.
3. **Test** board updates and collision accuracy.
4. **Integrate** with other modules and event bus seamlessly.

---

## Next Steps
- Continuously refine collision logic and board state handling.
- Expand board management documentation and examples.

