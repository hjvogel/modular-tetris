import sys, os, json, time, threading
import pygame

# TODO import all specific here tetris stuff from a main game (best of breed bundle) config
sys.path.extend([
    "./tetris-board-engine",
    "./tetris-move-controller",
    "./tetris-scoring-rules",
    "./tetris-game-state",
    "./tetris-ui-buttons"
])

from plugin_agent import PluginAgent
from event_bus import EventBus
import board, move, scoring, state, ui_headless as ui, buttons, play_loop

pygame.init()
clock = pygame.time.Clock()

agent = PluginAgent()
bus = EventBus()

# ⬅️ Inject the agent into state module so it can update score
state.inject_agent(agent)

agent.register_module("tetris-board-engine", board.handler)
agent.register_module("tetris-move-controller", move.handler)
agent.register_module("tetris-scoring-rules", scoring.handler)
agent.register_module("tetris-game-state", state.handler)
agent.register_module("tetris-ui-buttons", buttons.handler)

agent.register_module("play-loop", play_loop.handler)
agent.register_module("ui-headless", ui.handler)

bus.subscribe("button_press", state.handler)
bus.subscribe("state_change", board.handler)
bus.subscribe("move_action", board.handler)
bus.subscribe("piece_placed", scoring.handler)
bus.subscribe("score_update", ui.handler)

ui.ui.set_bus(bus)
ui.ui.initialize()

shared_state = {
    "game_running": False,
    "quit_game": False,
    "tick_number": 0
}

def handle_key_event(key):
    if not shared_state["game_running"]:
        return
    if key == pygame.K_LEFT:
        state.move("left")
    elif key == pygame.K_RIGHT:
        state.move("right")
    elif key == pygame.K_DOWN:
        state.move("down")
    elif key == pygame.K_UP:
        state.rotate()

def handle_button_click(button_id):
    if button_id == "start":
        shared_state.update({"game_running": True, "tick_number": 0})
        agent.handle_command(json.dumps({
            "command": "reset_score",
            "target_module": "tetris-scoring-rules"
        }))
        state.start()
    elif button_id == "pause":
        shared_state["game_running"] = not shared_state["game_running"]
    elif button_id == "quit":
        shared_state["quit_game"] = True

def on_game_tick(event_type, payload):
    if not shared_state["game_running"]:
        return

    shared_state["tick_number"] += 1
    state.tick()
    board_state = json.loads(agent.handle_command(json.dumps({
        "command": "get_board",
        "target_module": "tetris-board-engine"
    })))
    score_state = json.loads(agent.handle_command(json.dumps({
        "command": "get_score",
        "target_module": "tetris-scoring-rules"
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
                tick = json.loads(agent.handle_command(json.dumps({
                    "command": "create_tick",
                    "target_module": "play-loop"
                })))
                bus.publish("game_tick", "play-loop", tick)
                time.sleep(1)
        threading.Thread(target=loop_runner, daemon=True).start()

    if shared_state["quit_game"]:
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("[System] Pygame quit")
