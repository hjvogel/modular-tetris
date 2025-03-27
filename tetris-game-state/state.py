import json
import os
import random
from datetime import datetime
import board

# Will be injected by main
agent = None

class GameState:
    def __init__(self):
        self.state = "initialized"
        self.details = {}
        self.blocks = []
        self.current_block = None
        self.current_rotation = 0
        self.current_block_pos = [3, 0]

    def set_state(self, state, details=None):
        self.state = state
        self.details = details or {}
        return json.dumps({
            "event": "state_change",
            "source": "tetris-game-state",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "state": self.state,
            "details": self.details
        })

    def game_start(self, initial_level=1, initial_score=0):
        return self.set_state("game_start", {
            "initial_level": initial_level,
            "initial_score": initial_score
        })

    def pause_game(self):
        return self.set_state("paused", {
            "paused_at": datetime.utcnow().isoformat() + "Z"
        })

    def resume_game(self):
        return self.set_state("resumed", {
            "resumed_at": datetime.utcnow().isoformat() + "Z"
        })

    def game_over(self, reason, final_score, level_reached):
        return self.set_state("game_over", {
            "reason": reason,
            "final_score": final_score,
            "level_reached": level_reached
        })

    def load_blocks(self, directory="./tetris-blocks-data/examples/"):
        self.blocks = []
        for fname in os.listdir(directory):
            if fname.endswith("block.json"):
                with open(os.path.join(directory, fname)) as f:
                    self.blocks.append(json.load(f))
        return self.blocks

    def start(self):
        load_blocks()
        board.board.clear_grid()
        self.current_rotation = 0
        self.current_block = random.choice(self.blocks)
        self.current_block_pos = [3, 0]
        self.place()

    def tick(self):
        if not self.current_block:
            return
        shape = self.get_shape()
        self.erase(shape, self.current_block_pos)

        new_pos = [self.current_block_pos[0], self.current_block_pos[1] + 1]
        if not board.board.is_collision(shape, new_pos):
            self.current_block_pos = new_pos
        else:
            self.place()
            cleared = board.board.clear_lines()
            if cleared > 0 and agent:
                agent.handle_command(json.dumps({
                    "command": "update_score",
                    "target_module": "tetris-scoring-rules",
                    "parameters": {"lines": cleared}
                }))
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
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5)) if isinstance(color_hex, str) else (255, 0, 255)
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

game_state = GameState()

def handler(command, params):
    if command == "game_start":
        return game_state.game_start(
            initial_level=params.get("initial_level", 1),
            initial_score=params.get("initial_score", 0)
        )
    elif command == "pause_game":
        return game_state.pause_game()
    elif command == "resume_game":
        return game_state.resume_game()
    elif command == "game_over":
        return game_state.game_over(
            reason=params.get("reason", "unknown"),
            final_score=params.get("final_score", 0),
            level_reached=params.get("level_reached", 0)
        )
    elif command == "get_state":
        return json.dumps({
            "state": game_state.state,
            "details": game_state.details
        })

    return json.dumps({
        "error": "Unknown state command",
        "received": command
    })

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

def inject_agent(plugin_agent):
    global agent
    agent = plugin_agent
