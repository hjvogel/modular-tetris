### 📄 `AGENT_README.md`

```markdown
# Plugin Agent

## Overview

This plugin agent enables modular communication between components using a simple structured JSON interface. It routes commands from external clients, LLMs, or automation scripts to any registered modules.

The agent is fully decoupled from application-specific logic and can be reused across games, simulations, services, or interactive workflows.

---

## Structure

```
project-root/
├── plugin_agent.py
├── AGENT_README.md
├── examples/
│   └── example-command.json
```

---

## JSON Command Schema (`examples/example-command.json`)

```json
{
  "command": "rotate_object",
  "target_module": "physics-engine",
  "parameters": {
    "object_id": "cube-17",
    "angle": 90
  }
}
```

---

## plugin_agent.py

```python
import json

class PluginAgent:
    def __init__(self):
        self.modules = {}

    def register_module(self, name, handler_function):
        self.modules[name] = handler_function

    def handle_command(self, command_json):
        try:
            command = json.loads(command_json)
            module = command["target_module"]
            handler = self.modules.get(module)
            if handler is None:
                return json.dumps({"error": f"Module not found: {module}"})
            result = handler(command["command"], command.get("parameters", {}))
            return result
        except Exception as e:
            return json.dumps({"error": str(e)})
```

---

## Usage & Integration

- Acts as a command hub between external systems and internal modules
- Accepts structured commands and forwards them to the correct module
- Supports any kind of logic, from simulations to UI controls

---

## Example LLM Prompt (ReplacebAI)

```
"Send a structured command to the plugin agent to control an interactive simulation."
```

---

## Lean Integration Loop

1. **Define**: Clear JSON schemas for each module’s expected commands.
2. **Register**: Modules using `agent.register_module(...)`.
3. **Handle**: Calls with `agent.handle_command(json.dumps({...}))`.
4. **Extend**: Easily add new modules, logic, and external integrations.

---

## Next Steps

- Consider adding optional logging, permission control, or async support
- Integrate with GUI or WebSocket layers for real-time interactivity
