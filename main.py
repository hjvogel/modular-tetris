import sys, os, json, time, threading, random
import pygame

# Plugin system imports
sys.path.append("./tetris-plugin-agent")
sys.path.append("./tetris-event-bus")
sys.path.append("./tetris-board-engine")
sys.path.append("./tetris-move-controller")
sys.path.append("./tetris-scoring-rules")
sys.path.append("./tetris-game-state")
sys.path.append("./tetris-ui-headless")
sys.path.append("./tetris-ui-buttons")
sys.path.append("./tetris-play-loop")

from plugin_agent import PluginAgent
from event_bus import EventBus
import board
import move
import scoring
import state
import ui_headless as ui
import buttons
import play_loop

pygame.init()

CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT + 80))
pygame.display.set_caption("Modular Tetris")
clock = pygame.time.Clock()

# Load all blocks
BLOCKS_DIR = "./tetris-blocks-data/examples/"
block_files = [f for f in os.listdir(BLOCKS_DIR) if f.endswith("block.json")]
BLOCKS = []
for fname in block_files:
    with open(os.path.join(BLOCKS_DIR, fname)) as f:
        block = json.load(f)
        BLOCKS.append(block)
print(BLOCKS)
agent = PluginAgent()
bus = EventBus()

agent.register_module("tetris-board-engine", board.handler)
agent.register_module("tetris-move-controller", move.handler)
agent.register_module("tetris-scoring-rules", scoring.handler)
agent.register_module("tetris-game-state", state.handler)
agent.register_module("tetris-ui-buttons", buttons.handler)
agent.register_module("tetris-play-loop", play_loop.handler)
agent.register_module("tetris-ui-headless", ui.handler)

bus.subscribe("button_press", state.handler)
bus.subscribe("state_change", board.handler)
bus.subscribe("move_action", board.handler)
bus.subscribe("piece_placed", scoring.handler)
bus.subscribe("score_update", ui.handler)

ui.ui.set_bus(bus)
ui.ui.initialize(screen)

shared_state = {
    "game_running": False,
    "quit_game": False,
    "tick_number": 0,
    "block_active": False
}

current_block_pos = [3, 0]
current_rotation = 0
current_block = random.choice(BLOCKS)

def get_current_shape():
    return current_block["rotations"][current_rotation % 4]

def erase_block_from_board(shape, position):
    px, py = position
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                gx, gy = px + x, py + y
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    board.board.grid[gy][gx] = 0

def place_block(pos):
    color_hex = current_block.get("color", "#FF00FF")
    if isinstance(color_hex, str) and color_hex.startswith("#"):
        color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    else:
        color = (255, 0, 255)

    return agent.handle_command(json.dumps({
        "command": "place_piece",
        "target_module": "tetris-board-engine",
        "parameters": {
            "shape": get_current_shape(),
            "position": pos,
            "color": color
        }
    }))

def apply_movement(move_command):
    global current_block_pos
    shape = get_current_shape()
    erase_block_from_board(shape, current_block_pos)
    response = agent.handle_command(json.dumps({
        "command": move_command,
        "target_module": "tetris-move-controller",
        "parameters": {
            "position": current_block_pos
        }
    }))
    move_result = json.loads(response)
    new_pos = move_result["payload"]["new_position"]
    valid = json.loads(agent.handle_command(json.dumps({
        "command": "is_collision",
        "target_module": "tetris-board-engine",
        "parameters": {
            "shape": shape,
            "position": new_pos
        }
    })))
    if not valid["collision"]:
        current_block_pos[:] = new_pos
    place_block(current_block_pos)

def apply_rotation():
    global current_rotation
    print("[ROTATE] Attempt rotation")
    print("[ROTATE] Current rotation:", current_rotation)
    next_rotation = (current_rotation + 1) % 4
    rotated_shape = current_block["rotations"][next_rotation]
    print("[ROTATE] Next rotation index:", next_rotation)
    print("[ROTATE] Current position:", current_block_pos)

    erase_block_from_board(get_current_shape(), current_block_pos)

    collision_result = agent.handle_command(json.dumps({
        "command": "is_collision",
        "target_module": "tetris-board-engine",
        "parameters": {
            "shape": rotated_shape,
            "position": current_block_pos
        }
    }))
    print("[ROTATE] Collision response:", collision_result)
    collision = json.loads(collision_result)

    if not collision.get("collision"):
        print("[ROTATE] No collision, applying rotation")
        current_rotation = next_rotation
        place_block(current_block_pos)
    else:
        print("[ROTATE] Rotation blocked due to collision")
        place_block(current_block_pos)

def handle_key_event(key):
    if not shared_state["game_running"]:
        return
    if key == pygame.K_LEFT:
        apply_movement("move_left")
    elif key == pygame.K_RIGHT:
        apply_movement("move_right")
    elif key == pygame.K_DOWN:
        apply_movement("move_down")
    elif key == pygame.K_UP:
        apply_rotation()

def handle_button_click(button_id):
    global current_rotation, current_block
    if button_id == "start":
        shared_state["game_running"] = True
        shared_state["block_active"] = True
        shared_state["tick_number"] = 0
        current_block_pos[0] = 3
        current_block_pos[1] = 0
        current_rotation = 0
        current_block = random.choice(BLOCKS)
        board.board.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        agent.handle_command(json.dumps({
            "command": "reset_score",
            "target_module": "tetris-scoring-rules",
            "parameters": {}
        }))
        place_block(current_block_pos)
    elif button_id == "pause":
        shared_state["game_running"] = not shared_state["game_running"]
    elif button_id == "quit":
        shared_state["quit_game"] = True

def on_game_tick(event_type, payload):
    global current_block, current_rotation

    if not shared_state["game_running"]:
        return

    shared_state["tick_number"] += 1

    shape = get_current_shape()
    erase_block_from_board(shape, current_block_pos)

    response = agent.handle_command(json.dumps({
        "command": "move_down",
        "target_module": "tetris-move-controller",
        "parameters": {
            "position": current_block_pos
        }
    }))
    move_result = json.loads(response)
    new_pos = move_result["payload"]["new_position"]

    collision = json.loads(agent.handle_command(json.dumps({
        "command": "is_collision",
        "target_module": "tetris-board-engine",
        "parameters": {
            "shape": shape,
            "position": new_pos
        }
    })))

    if not collision["collision"]:
        current_block_pos[:] = new_pos
    else:
        place_block(current_block_pos)
        cleared = json.loads(agent.handle_command(json.dumps({
            "command": "clear_lines",
            "target_module": "tetris-board-engine",
            "parameters": {}
        })))
        if cleared["cleared"] > 0:
            agent.handle_command(json.dumps({
                "command": "update_score",
                "target_module": "tetris-scoring-rules",
                "parameters": {"lines": cleared["cleared"]}
            }))
        current_block = random.choice(BLOCKS)
        current_block_pos[0] = 3
        current_block_pos[1] = 0
        current_rotation = 0

    place_block(current_block_pos)

    board_state = json.loads(agent.handle_command(json.dumps({
        "command": "get_board",
        "target_module": "tetris-board-engine",
        "parameters": {}
    })))
    score_state = json.loads(agent.handle_command(json.dumps({
        "command": "get_score",
        "target_module": "tetris-scoring-rules",
        "parameters": {}
    })))
    ui.ui.render_board(board_state, score_state)

bus.subscribe("game_tick", on_game_tick)

running = True
play_loop_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            clicked = ui.ui.handle_click((x, y))
            if clicked:
                handle_button_click(clicked)
        elif event.type == pygame.KEYDOWN:
            handle_key_event(event.key)

    if not play_loop_started:
        play_loop_started = True

        def loop_runner():
            for _ in range(999):
                tick_event_raw = agent.handle_command(json.dumps({
                    "command": "create_tick",
                    "target_module": "tetris-play-loop",
                    "parameters": {}
                }))
                try:
                    tick_event = json.loads(tick_event_raw)
                    payload = {
                        "tick_number": tick_event.get("tick_number"),
                        "timestamp": tick_event.get("timestamp")
                    }
                    bus.publish("game_tick", "tetris-play-loop", payload)
                except Exception as e:
                    print("[Loop] Tick parse error:", e)
                time.sleep(1)

        threading.Thread(target=loop_runner, daemon=True).start()

    if shared_state["quit_game"]:
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("[System] Pygame quit")
