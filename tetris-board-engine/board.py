import json

class TetrisBoard:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def is_collision(self, piece_shape, position):
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    gx, gy = px + x, py + y
                    if gx < 0 or gx >= self.width or gy >= self.height:
                        return True
                    if gy >= 0 and self.grid[gy][gx]:
                        return True
        return False

    def place_piece(self, piece_shape, position, color=(255, 0, 255)):
        if self.is_collision(piece_shape, position):
            return False
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    gx, gy = px + x, py + y
                    if 0 <= gx < self.width and 0 <= gy < self.height:
                        self.grid[gy][gx] = color  # <- stores color
        return True


    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared = self.height - len(new_grid)
        while len(new_grid) < self.height:
            new_grid.insert(0, [0] * self.width)
        self.grid = new_grid
        return cleared

    def get_board_state(self):
        return {
            "width": self.width,
            "height": self.height,
            "grid": self.grid
        }

board = TetrisBoard()

def handler(command, params):
    if command == "place_piece":
        shape = params.get("shape")
        position = params.get("position")
        color = params.get("color", "#FF00FF")
        if isinstance(color, str) and color.startswith("#"):
            color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        success = board.place_piece(shape, position, color)
        return json.dumps({"placed": success, "grid": board.grid})

    elif command == "clear_lines":
        cleared = board.clear_lines()
        return json.dumps({"cleared": cleared})

    elif command == "get_board":
        return json.dumps(board.get_board_state())

    elif command == "is_collision":
        shape = params.get("shape")
        position = params.get("position")
        result = board.is_collision(shape, position)
        return json.dumps({"collision": result})

    return json.dumps({"error": "Unknown board command", "received": command})