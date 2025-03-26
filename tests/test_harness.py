import os
import sys
import json

# Resolve path to plugin_agent in the same folder as this script
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_root)

from plugin_agent import PluginAgent
from event_bus import EventBus

# Dummy handlers for testing
def mock_handler(name):
    def handler(command, params):
        print(f"[{name}] Received command '{command}' with params {params}")
        return json.dumps({"status": "ok", "module": name, "command": command})
    return handler

# Register plugin modules
agent = PluginAgent()
agent.register_module("tetris-board-engine", mock_handler("board"))
agent.register_module("tetris-move-controller", mock_handler("move"))
agent.register_module("tetris-scoring-rules", mock_handler("score"))
agent.register_module("tetris-game-state", mock_handler("state"))
agent.register_module("tetris-ui-buttons", mock_handler("buttons"))
agent.register_module("tetris-play-loop", mock_handler("loop"))
agent.register_module("tetris-event-bus", mock_handler("bus"))

# Test command sequence
commands = [
    {
        "command": "start",
        "target_module": "tetris-ui-buttons",
        "parameters": {"button_id": "start"}
    },
    {
        "command": "move_left",
        "target_module": "tetris-move-controller",
        "parameters": {"piece_id": "T", "position": [4, 0], "rotation": 0}
    },
    {
        "command": "rotate",
        "target_module": "tetris-move-controller",
        "parameters": {"piece_id": "T", "position": [3, 0], "rotation": 0}
    }
]

# Execute test commands
for cmd in commands:
    print("\n--- Sending Command ---")
    response = agent.handle_command(json.dumps(cmd))
    print("Response:", response)
