import json

class TetrisBoard:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0]*width for _ in range(height)]

    def is_collision(self, piece_shape, position):
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    if (px+x < 0 or px+x >= self.width or
                        py+y >= self.height or
                        self.grid[py+y][px+x]):
                        return True
        return False

    def place_piece(self, piece_shape, position):
        if self.is_collision(piece_shape, position):
            return False
        px, py = position
        for y, row in enumerate(piece_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[py+y][px+x] = cell
        return True

    def get_board_state(self):
        return json.dumps({
            "width": self.width,
            "height": self.height,
            "grid": self.grid
        })

# Example usage with pygame (pseudo-integration)
# board = TetrisBoard()
# piece_shape = [[0,1,0],[1,1,1]] # T-piece
# position = [4, 0]
# print(board.place_piece(piece_shape, position))
# print(board.get_board_state())