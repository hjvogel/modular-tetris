
import pygame
import json
import time

CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
BUTTON_HEIGHT = 40

class UIHeadless:
    def __init__(self):
        print("UIHeadless init")
        self.screen = None
        self.font = None
        self.buttons = []
        self.bus = None

    def set_bus(self, bus):
        self.bus = bus

    def initialize(self, screen):
        print("UIHeadless initialize")
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.buttons = [
            {"id": "start", "label": "Start", "pos": (10, GRID_HEIGHT * CELL_SIZE + 5)},
            {"id": "pause", "label": "Pause", "pos": (110, GRID_HEIGHT * CELL_SIZE + 5)},
            {"id": "quit", "label": "Quit", "pos": (210, GRID_HEIGHT * CELL_SIZE + 5)},
        ]
        self.render_buttons()

    def render_board(self, board_state, score_state=None):
        grid = board_state.get("grid", [])
        if not self.screen:
            print("[UI] Cannot render board, screen not initialized")
            return

        self.screen.fill((0, 0, 0))

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if isinstance(cell, (tuple, list)) and len(cell) == 3:
                    color = tuple(cell)
                elif isinstance(cell, str) and cell.startswith("#") and len(cell) == 7:
                    try:
                        color = tuple(int(cell[i:i+2], 16) for i in (1, 3, 5))
                    except:
                        color = (255, 0, 255)
                elif isinstance(cell, int) and cell != 0:
                    color = (200, 200, 200)
                else:
                    continue  # empty cell

                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

        self.render_buttons()
        if score_state:
            self.render_score(score_state)

        pygame.display.update()

    def render_score(self, score_state):
        if not self.font:
            print("[UI] Font not initialized")
            return
        text = f"Score: {score_state.get('total_score', 0)}"
        label = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(label, (10, GRID_HEIGHT * CELL_SIZE + BUTTON_HEIGHT + 5))

    def render_buttons(self):
        for btn in self.buttons:
            rect = pygame.Rect(btn["pos"][0], btn["pos"][1], 80, BUTTON_HEIGHT)
            pygame.draw.rect(self.screen, (80, 80, 200), rect)
            text = self.font.render(btn["label"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        for btn in self.buttons:
            rect = pygame.Rect(btn["pos"][0], btn["pos"][1], 80, BUTTON_HEIGHT)
            if rect.collidepoint(pos):
                print(f"[UI] Button clicked: {btn['id']}")
                if self.bus:
                    event = {
                        "event": "button_press",
                        "source": "ui_headless",
                        "button_id": btn["id"],
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    }
                    self.bus.publish("button_press", "ui_headless", event)
                return btn["id"]
        return None

ui = UIHeadless()

def handler(command, params):
    if command == "init_ui":
        screen = params.get("screen")
        ui.initialize(screen)
        return json.dumps({"status": "ui_initialized"})

    elif command == "render_board":
        board_state = params.get("board_state", {})
        score_state = params.get("score_state", {})
        ui.render_board(board_state, score_state)
        return json.dumps({"status": "board_rendered"})

    elif command == "score_update":
        ui.render_score(params)
        pygame.display.update()
        return json.dumps({"status": "score_rendered"})

    return json.dumps({
        "error": "Unknown UI command",
        "received": command
    })