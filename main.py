import sys, os, json, time, threading
import pygame

# Load general game config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "tetris-config", "game_config.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Setup pygame
pygame.init()
clock = pygame.time.Clock()

# Dynamically load plugins paths
for path in config["plugin_paths"]:
    sys.path.append(path)

from plugin_agent import PluginAgent
from event_bus import EventBus
import ui_headless as ui

# Dynamically import configured plugins
plugins = {}
for module in config["modules"]:
    mod = __import__(module["import_name"])
    plugins[module["name"]] = mod

agent = PluginAgent()
bus = EventBus()

# Inject agent into state module (mandatory for scoring updates)
if hasattr(plugins[config["state_module"]], "inject_agent"):
    plugins[config["state_module"]].inject_agent(agent)
# After injecting agent
if hasattr(plugins[config["state_module"]], "inject_bus"):
    plugins[config["state_module"]].inject_bus(bus)


# Register modules
for module in config["modules"]:
    agent.register_module(module["name"], plugins[module["name"]].handler)

# Subscribe events
for sub in config["event_subscriptions"]:
    bus.subscribe(sub["event_type"], plugins[sub["target_module"]].handler)

# Setup UI
ui.ui.set_bus(bus)
ui.ui.initialize(config)

shared_state = {
    "game_running": False,
    "quit_game": False,
    "tick_number": 0
}

def handle_key_event(key):
    if not shared_state["game_running"]:
        return
    key_mapping = {
        pygame.K_LEFT: ("move", {"direction": "left"}),
        pygame.K_RIGHT: ("move", {"direction": "right"}),
        pygame.K_DOWN: ("move", {"direction": "down"}),
        pygame.K_UP: ("rotate", {})
    }
    action = key_mapping.get(key)
    if action:
        command, params = action
        plugins[config["state_module"]].handler(command, params)


def handle_button_click(button_id):
    action = config["button_actions"].get(button_id)
    if action == "start":
        print("[Main] Start button clicked")
        shared_state.update({"game_running": True, "tick_number": 0})
        agent.handle_command(json.dumps({
            "command": "reset_score",
            "target_module": config["scoring_module"]
        }))
        plugins[config["state_module"]].start()
    elif action == "pause":
        print("[Main] Pause button clicked")
        shared_state["game_running"] = not shared_state["game_running"]
    elif action == "quit":
        print("[Main] Quit button clicked")
        shared_state["quit_game"] = True

def on_game_tick(event_type, payload):
    if not shared_state["game_running"]:
        return
    shared_state["tick_number"] += 1
    plugins[config["state_module"]].tick()

    board_state = json.loads(agent.handle_command(json.dumps({
        "command": config["board_get_command"],
        "target_module": config["board_module"]
    })))

    score_state = json.loads(agent.handle_command(json.dumps({
        "command": config["score_get_command"],
        "target_module": config["scoring_module"]
    })))

    ui.ui.render_board(board_state, score_state)

bus.subscribe("game_tick", on_game_tick)

# Main game loop
running = True
play_loop_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = ui.ui.handle_click(event.pos)
            if clicked:
                handle_button_click(clicked)
        elif event.type == pygame.KEYDOWN:
            handle_key_event(event.key)

    if not play_loop_started:
        play_loop_started = True
        def loop_runner():
            for _ in range(config["tick_count"]):
                tick = json.loads(agent.handle_command(json.dumps({
                    "command": config["tick_create_command"],
                    "target_module": config["loop_module"]
                })))
                bus.publish("game_tick", config["loop_module"], tick)
                time.sleep(config["tick_interval"])
        threading.Thread(target=loop_runner, daemon=True).start()

    if shared_state["quit_game"]:
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("[System] Game exited.")
