import json

# Directional offsets
OFFSETS = {
    "left": (-1, 0),
    "right": (1, 0),
    "down": (0, 1),
    "rotate": (0, 0),  # Stub: No real rotation yet
    "drop": (0, 999)   # Extreme drop, to be clamped by collision check
}

def handler(command, params):
    if command.startswith("move_") or command in ["rotate", "drop"]:
        move_type = command.split("_")[-1] if "_" in command else command
        offset = OFFSETS.get(move_type, (0, 0))

        current_pos = params.get("position", [0, 0])
        px, py = current_pos
        dx, dy = offset

        new_position = [px + dx, py + dy]

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

    return json.dumps({
        "error": "Unknown move command",
        "received": command
    })
