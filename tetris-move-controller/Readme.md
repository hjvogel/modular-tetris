# Tetris Move Controller Repo

## Overview

This repository manages player input processing for a modular Tetris game, converting player actions into standardized events for easy integration with other Tetris modules and LLM-based plugins.

## Repo Structure

```
tetris-move-controller/
├── README.md
├── schema.json
├── controller.py
└── examples/
    ├── move-left.json
    ├── move-right.json
    └── rotate-piece.json
```

## JSON Schema (`schema.json`)

Defines the structure for move-related events:

```json
{
  "event": "string",
  "action": "string",
  "piece_id": "string",
  "position": "array",
  "rotation": "integer"
}
```

## Example Move Actions

### Move Left (`move-left.json`)

```json
{
  "event": "move_action",
  "action": "move_left",
  "piece_id": "T",
  "position": [4, 0],
  "rotation": 0
}
```

### Move Right (`move-right.json`)

```json
{
  "event": "move_action",
  "action": "move_right",
  "piece_id": "L",
  "position": [3, 0],
  "rotation": 90
}
```

### Rotate Piece (`rotate-piece.json`)

```json
{
  "event": "move_action",
  "action": "rotate",
  "piece_id": "J",
  "position": [5, 2],
  "rotation": 180
}
```

## Usage & Integration

Process player inputs and broadcast standardized events to other Tetris modules, facilitating gameplay synchronization and response handling.

### Example LLM Integration Prompt (ReplacebAI)

```
"Process player inputs into standardized game events such as move and rotate actions."
```

## controller.py

```python
import json

class MoveController:
    def __init__(self):
        pass

    def create_move_event(self, action, piece_id, position, rotation):
        event = {
            "event": "move_action",
            "action": action,
            "piece_id": piece_id,
            "position": position,
            "rotation": rotation
        }
        return json.dumps(event)

    def move_left(self, piece_id, position, rotation):
        position[0] -= 1
        return self.create_move_event("move_left", piece_id, position, rotation)

    def move_right(self, piece_id, position, rotation):
        position[0] += 1
        return self.create_move_event("move_right", piece_id, position, rotation)

    def rotate_piece(self, piece_id, position, rotation):
        rotation = (rotation + 90) % 360
        return self.create_move_event("rotate", piece_id, position, rotation)

# Example usage with pygame (pseudo-integration)
# controller = MoveController()
# print(controller.move_left("T", [4,0], 0))
# print(controller.rotate_piece("J", [5,2], 90))
```

## Lean Development Loop