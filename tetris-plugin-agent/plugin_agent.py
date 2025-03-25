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