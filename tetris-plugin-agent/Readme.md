# Tetris Plugin Agent Repo

## Overview

This repository provides an agent interface for integrating modular Tetris components with LLMs, automation scripts, or external APIs. It enables conversational control, structured input/output, and plugin extensibility via a simple interface.

## Repo Structure

```
tetris-plugin-agent/
├── README.md
├── schema.json
├── plugin_agent.py
└── examples/
    └── plugin-command.json
```

## JSON Schema (`schema.json`)

Defines the structure for LLM or external system commands:

```json
{
  "command": "string",
  "target_module": "string",
  "parameters": "object"
}
```

## Example Plugin Command (`plugin-command.json`)

```json
{
  "command": "move_left",
  "target_module": "tetris-move-controller",
  "parameters": {
    "piece_id": "T",
    "position": [4, 0],
    "rotation": 0
  }
}
```

## Usage & Integration

Use this agent to relay structured commands between LLMs, external clients, or system events and specific Tetris modules.

### Example LLM Integration Prompt (ReplacebAI)

```
"Send a structured command to control Tetris gameplay via the plugin agent interface."
```

## plugin_agent.py

```python
import json

class PluginAgent:
    def __init__(self):
        self.modules = {}

    def register_module(self, name, handler):
        self.modules[name] = handler

    def handle_command(self, command_json):
        command_data = json.loads(command_json)
        target = command_data.get("target_module")
        if target in self.modules:
            handler = self.modules[target]
            return handler(command_data.get("command"), command_data.get("parameters"))
        return json.dumps({"error": "Module not found"})

# Example usage (pseudo)
# def move_controller_handler(command, params):
#     return json.dumps({"status": "moved", "action": command, "details": params})
#
# agent = PluginAgent()
# agent.register_module("tetris-move-controller", move_controller_handler)
# print(agent.handle_command(json.dumps({
#     "command": "move_left",
#     "target_module": "tetris-move-controller",
#     "parameters": {"piece_id": "T", "position": [4, 0], "rotation": 0}
# })))
```

## Lean Development Loop

1. **Define** plugin command schemas for structured communication.
2. **Develop** command routing and dispatch logic.
3. **Test** LLM interactions and plugin extensibility.
4. **Integrate** with internal modules and external LLM interfaces.

---

## Next Steps
- Expand compatibility with plugin-based UIs or LLM frameworks.
- Refine routing and fallback logic for dynamic agent interaction.

