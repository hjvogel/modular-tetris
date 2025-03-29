import json
import os
import random
from datetime import datetime
import board

agent = None  # Injected by main.py

class GameState:
    def __init__(self):
        self.state = "initialized"
        self.details = {}
        self.blocks = []
        self.current_block = None
        self.current_rotation = 0
        self.current_block_pos = [3, 0]

    def load_blocks(self, directory="./tetris-blocks-data/examples/"):
        self.blocks = []
        for fname in os.listdir(directory):
            if fname.endswith(".json"):
                with open(os.path.join(directory, fname)) as f:
                    self.blocks.append(json.load(f))

    def start(self):
        self.load_blocks()
        board.board.clear_grid()
        self.current_block = random.choice(self.blocks)
        self.current_rotation = 0
        self.current_block_pos = [3, 0]
        self.place()

    def tick(self):
        shape = self.get_shape()
        self.erase(shape, self.current_block_pos)

        new_pos = [self.current_block_pos[0], self.current_block_pos[1] + 1]
        if not board.board.is_collision(shape, new_pos):
            self.current_block_pos = new_pos
        else:
            self.place()
            cleared = board.board.clear_lines()
            if cleared > 0:
                print(f"[State] Clearing {cleared} lines")
                self.update_score(cleared)
            self.current_block = random.choice(self.blocks)
            self.current_rotation = 0
            self.current_block_pos = [3, 0]
        self.place()

    def move(self, direction):
        shape = self.get_shape()
        offset = {"left": (-1, 0), "right": (1, 0), "down": (0, 1)}.get(direction, (0, 0))
        new_pos = [self.current_block_pos[0] + offset[0], self.current_block_pos[1] + offset[1]]
        self.erase(shape, self.current_block_pos)
        if not board.board.is_collision(shape, new_pos):
            self.current_block_pos = new_pos
        self.place()

    def rotate(self):
        next_rotation = (self.current_rotation + 1) % len(self.current_block["rotations"])
        rotated = self.current_block["rotations"][next_rotation]
        self.erase(self.get_shape(), self.current_block_pos)
        if not board.board.is_collision(rotated, self.current_block_pos):
            self.current_rotation = next_rotation
        self.place()

    def place(self):
        color_hex = self.current_block.get("color", "#FF00FF")
        if isinstance(color_hex, str) and color_hex.startswith("#"):
            color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
        else:
            color = (255, 0, 255)
        board.board.place_piece(self.get_shape(), self.current_block_pos, color)

    def erase(self, shape, position):
        px, py = position
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    gx, gy = px + x, py + y
                    if 0 <= gx < board.board.width and 0 <= gy < board.board.height:
                        board.board.grid[gy][gx] = 0

    def get_shape(self):
        return self.current_block["rotations"][self.current_rotation % len(self.current_block["rotations"])]

    def update_score(self, lines_cleared):
        global agent
        if agent:
            response = agent.handle_command(json.dumps({
                "command": "update_score",
                "target_module": "scoring-rules",
                "parameters": {"lines": lines_cleared}
            }))
            print(f"[State] Score update response: {response}")

game_state = GameState()

def handler(command, params):
    if command == "game_start":
        game_state.start()
        return json.dumps({"status": "game_started"})
    elif command == "move":
        game_state.move(params["direction"])
        return json.dumps({"status": f"moved {params['direction']}"})
    elif command == "rotate":
        game_state.rotate()
        return json.dumps({"status": "rotated"})
    elif command == "tick":
        game_state.tick()
        return json.dumps({"status": "tick_complete"})
    return json.dumps({"error": "Unknown state command", "received": command})

def inject_agent(plugin_agent):
    global agent
    agent = plugin_agent

# Necessary standalone functions for main.py compatibility
def load_blocks(directory="./tetris-blocks-data/examples/"):
    return game_state.load_blocks(directory)

def start():
    return game_state.start()

def tick():
    return game_state.tick()

def move(direction):
    return game_state.move(direction)

def rotate():
    return game_state.rotate()
