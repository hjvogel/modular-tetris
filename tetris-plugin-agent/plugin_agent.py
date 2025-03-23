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