# tetris-move-controller/move.py

import json

OFFSETS = {
    "left": (-1, 0),
    "right": (1, 0),
    "down": (0, 1),
    "rotate": (0, 0),
    "drop": (0, 999)
}

def apply_movement(command, position):
    move_type = command.split("_")[-1] if "_" in command else command
    offset = OFFSETS.get(move_type, (0, 0))
    px, py = position
    dx, dy = offset
    return [px + dx, py + dy]

def handler(command, params):
    if command.startswith("move_") or command in ["rotate", "drop"]:
        move_type = command.split("_")[-1] if "_" in command else command
        offset = OFFSETS.get(move_type, (0, 0))
        current_pos = params.get("position", [0, 0])
        new_position = apply_movement(command, current_pos)

        result = {
            "event": "move_action",
            "source": "tetris-move-controller",
            "payload": {
                "move": move_type,
                "previous": current_pos,
                "new_position": new_position,
                "offset": offset,
                "rotate": (move_type == "rotate"),
                "drop": (move_type == "drop")
            }
        }
        return json.dumps(result)

    elif command == "apply_movement":
        current_pos = params.get("position", [0, 0])
        move_type = params.get("move_type", "down")
        new_pos = apply_movement(move_type, current_pos)
        return json.dumps({"new_position": new_pos})

    return json.dumps({
        "error": "Unknown move command",
        "received": command
    })
