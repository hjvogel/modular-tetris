# UI Headless Module

## Overview

This module provides a **headless UI rendering system** designed for use in modular, pluggable game systems. It enables flexible integration with Pygame or similar engines without assuming any game-specific semantics like "Tetris". Layout and sizing are controlled through external JSON configuration files.

## File Structure

```
root/
├── ui_headless.py
├── tetris-board-engine/
│   └── tetris_ui_config.json
├── examples/
│   ├── render-board.json
│   └── ui-event.json
├── UI_HEADLESS_README.md
```

## Config File (`tetris_ui_config.json`)

This file defines rendering layout settings. It is referenced at runtime and can be modified to suit different games or environments.

```json
{
  "grid_width": 10,
  "grid_height": 20,
  "cell_size": 30,
  "button_height": 40
}
```

## JSON Schema (`examples/ui-event.json`)

Defines standard format for button events and UI interaction:

```json
{
  "action": "button_press",
  "ui_elements": [
    {"type": "button", "id": "start"},
    {"type": "button", "id": "pause"},
    {"type": "button", "id": "quit"}
  ]
}
```

## Example Board Render Event (`examples/render-board.json`)

```json
{
  "action": "render_board",
  "board_state": {
    "width": 10,
    "height": 20,
    "grid": [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ...
    ]
  }
}
```

## Usage

- Call `ui.initialize(screen)` with a Pygame surface.
- Call `ui.render_board(board_state)` to update screen visuals.
- Call `ui.render_score(score_state)` to display score.
- Handle mouse input with `ui.handle_click(position)`.

## LLM Integration Example Prompt

```
"Render the current game board and UI state using the headless renderer. Handle button interactions based on user input."
```

## Headless API: `ui_headless.py`

```python
def initialize(screen): 
    # Setup fonts, layout, and buttons from config

def render_board(board_state, score_state=None): 
    # Draw grid cells, colored blocks, and score if given

def render_buttons(): 
    # Draw UI buttons with labels

def handle_click(position): 
    # Check if a button was clicked and return event
```

## Lean Integration Steps

1. **Define** UI layout in `tetris_ui_config.json`.
2. **Develop** rendering logic decoupled from game domain.
3. **Connect** UI event handling via a pub-sub bus or callbacks.
4. **Extend** with new buttons, overlays, or modes.

---

## Next Steps

- Add alternate render modes (e.g., gridlines, debug overlays).
- Enable config hot-reload without restarting game engine.
- Allow headless event export for automated testing or LLM-driven play.
