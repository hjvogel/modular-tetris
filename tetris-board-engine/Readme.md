# Tetris Board Engine Repo

## Overview

This repository handles board state management, collision detection, and piece placement for a modular Tetris game, clearly structured for integration with other Tetris modules and optimized for easy interaction with LLM-based plugins.

## Repo Structure

```
tetris-board-engine/
├── README.md
├── schema.json
├── board.py
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
        self.grid = [[0]*width for _ in range(height)]

    def is_collision(self, piece_shape, position):
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    if (px+x < 0 or px+x >= self.width or
                        py+y >= self.height or
                        self.grid[py+y][px+x]):
                        return True
        return False

    def place_piece(self, piece_shape, position):
        if self.is_collision(piece_shape, position):
            return False
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[py+y][px+x] = cell
        return True

    def get_board_state(self):
        return json.dumps({
            "width": self.width,
            "height": self.height,
            "grid": self.grid
        })

# Example usage with pygame (pseudo-integration)
# board = TetrisBoard()
# piece_shape = [[0,1,0],[1,1,1]] # T-piece
# position = [4, 0]
# print(board.place_piece(piece_shape, position))
# print(board.get_board_state())
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

