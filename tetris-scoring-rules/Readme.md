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

class ScoringSystem:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0

    def update_score(self, lines_cleared):
        points_per_line = {1: 100, 2: 300, 3: 500, 4: 800}
        gained_score = points_per_line.get(lines_cleared, 0) * self.level
        self.score += gained_score
        self.lines_cleared_total += lines_cleared
        self.level = self.lines_cleared_total // 10 + 1

        event = {
            "event": "score_update",
            "score": self.score,
            "lines_cleared": lines_cleared,
            "level": self.level
        }
        return json.dumps(event)

# Example usage with pygame (pseudo-integration)
# scoring = ScoringSystem()
# print(scoring.update_score(2))
# print(scoring.update_score(4))
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

