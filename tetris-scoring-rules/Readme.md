# Tetris Scoring Rules Repo

## Overview

This repository manages scoring calculations and updates for a modular Tetris game, clearly structured for integration with other Tetris modules and optimized for easy interaction with LLM-based plugins.

## Repo Structure

```
tetris-scoring-rules/
├── README.md
├── schema.json
├── scoring.py
└── examples/
    ├── score-update.json
    └── lines-cleared.json
```

## JSON Schema (`schema.json`)

Defines the structure for score-related events:

```json
{
  "event": "string",
  "score": "integer",
  "lines_cleared": "integer",
  "level": "integer"
}
```

## Example Scoring Events

### Score Update (`score-update.json`)

```json
{
  "event": "score_update",
  "score": 1200,
  "lines_cleared": 3,
  "level": 2
}
```

### Lines Cleared (`lines-cleared.json`)

```json
{
  "event": "lines_cleared",
  "score": 800,
  "lines_cleared": 2,
  "level": 1
}
```

## Usage & Integration

Calculate and broadcast scoring updates across Tetris modules by sending standardized JSON events.

### Example LLM Integration Prompt (ReplacebAI)

```
"Calculate scoring updates based on gameplay events, lines cleared, and current level."
```

## scoring.py

```python
import json

LINE_SCORES = {
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}

score_state = {
    "lines_cleared": 0,
    "total_score": 0,
    "level": 1
}

def update_score(lines):
    score_gain = LINE_SCORES.get(lines, 0)
    score_state["lines_cleared"] += lines
    score_state["total_score"] += score_gain
    return score_state

def reset_score():
    score_state["lines_cleared"] = 0
    score_state["total_score"] = 0
    score_state["level"] = 1
    return score_state

def handler(command, params):
    if command == "update_score":
        lines = params.get("lines", 0)
        updated = update_score(lines)
        return json.dumps({
            "event": "score_update",
            "source": "tetris-scoring-rules",
            "payload": updated
        })
    elif command == "get_score":
        return json.dumps(score_state)
    elif command == "reset_score":
        reset = reset_score()
        return json.dumps({
            "event": "score_reset",
            "source": "tetris-scoring-rules",
            "payload": reset
        })
    return json.dumps({
        "error": "Unknown scoring command",
        "received": command
    })
```

## Lean Development Loop

1. **Define** clear and concise JSON schemas.
2. **Develop** robust scoring calculation logic.
3. **Test** event broadcasting and scoring accuracy.
4. **Integrate** smoothly with other modules and event bus.

---

## Next Steps
- Continuously refine scoring logic based on gameplay feedback.
- Expand scoring rules documentation and examples.

