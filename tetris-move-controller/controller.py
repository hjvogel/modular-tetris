import json

class MoveController:
    def __init__(self):
        pass

    def create_move_event(self, action, piece_id, position, rotation):
        event = {
            "event": "move_action",
            "action": action,
            "piece_id": piece_id,
            "position": position,
            "rotation": rotation
        }
        return json.dumps(event)

    def move_left(self, piece_id, position, rotation):
        position[0] -= 1
        return self.create_move_event("move_left", piece_id, position, rotation)

    def move_right(self, piece_id, position, rotation):
        position[0] += 1
        return self.create_move_event("move_right", piece_id, position, rotation)

    def rotate_piece(self, piece_id, position, rotation):
        rotation = (rotation + 90) % 360
        return self.create_move_event("rotate", piece_id, position, rotation)

# Example usage with pygame (pseudo-integration)
# controller = MoveController()
# print(controller.move_left("T", [4,0], 0))
# print(controller.rotate_piece("J", [5,2], 90))