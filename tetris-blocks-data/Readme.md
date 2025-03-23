# Tetris Blocks Data Repo

## Overview

This repository contains standardized definitions for all Tetris blocks (tetrominoes), structured for easy modular integration and efficient usage by both developers and LLM-driven plugins.

## Repo Structure

```
tetris-blocks-data/
├── README.md
├── schema.json
└── examples/
    ├── I-block.json
    ├── T-block.json
    ├── L-block.json
    ├── J-block.json
    ├── O-block.json
    ├── S-block.json
    └── Z-block.json
```

## JSON Schema (`schema.json`)

Defines the tetromino blocks with shapes, colors, and possible rotations:

```json
{
  "id": "string",
  "shape": "array",
  "color": "string",
  "rotations": "array"
}
```

## Example Block (`T-block.json`)

```json
{
  "id": "T",
  "shape": [
    [0, 1, 0],
    [1, 1, 1]
  ],
  "color": "#FF00FF",
  "rotations": [
    [[0,1,0],[1,1,1]],
    [[1,0],[1,1],[1,0]],
    [[1,1,1],[0,1,0]],
    [[0,1],[1,1],[0,1]]
  ]
}
```

## Usage & Integration

Fetch and import block data directly into your Tetris modules or LLM-based plugins. Use provided JSON files for immediate integration.

### Example LLM Integration Prompt (ReplacebAI)

```
"Retrieve Tetris block definitions and rotations by block ID."
```

## Lean Development Loop

1. **Define** clear and concise JSON schema.
2. **Develop** complete block examples.
3. **Test** JSON integrity and usability.
4. **Integrate** seamlessly with other Tetris modules.

---

## Next Steps
- Continue refining based on module integration feedback.
- Expand documentation and examples for improved clarity.

