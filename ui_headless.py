import pygame, json, time

class UIHeadless:
    def __init__(self):
        self.screen = None
        self.font = None
        self.buttons = []
        self.bus = None
        self.config = {}

    def set_bus(self, bus):
        self.bus = bus

    def initialize(self, config):
        print("[UI] Initializing UI from config")
        self.config = config
        ui_cfg = config["ui_config"]
        pygame.display.set_caption(config["game_name"])
        size = (ui_cfg["grid_width"]*ui_cfg["cell_size"],
                ui_cfg["grid_height"]*ui_cfg["cell_size"]+ui_cfg["button_height"]+50)
        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont(ui_cfg["font"], ui_cfg["font_size"])
        self.buttons = ui_cfg["buttons"]
        self.render_buttons()

    def render_board(self, board_state, score_state=None):
        self.screen.fill(self.config["ui_config"]["bg_color"])
        cell_size = self.config["ui_config"]["cell_size"]
        grid = board_state.get("grid", [])

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell:
                    color = cell if isinstance(cell, (tuple, list)) else self.config["ui_config"]["colors"]["default"]
                    pygame.draw.rect(self.screen, color, (x*cell_size, y*cell_size, cell_size, cell_size))
        self.render_buttons()
        if score_state:
            self.render_score(score_state)
        pygame.display.flip()

    def render_buttons(self):
        for btn in self.buttons:
            rect = pygame.Rect(btn["pos"], (80, self.config["ui_config"]["button_height"]))
            pygame.draw.rect(self.screen, (80,80,200), rect)
            label = self.font.render(btn["label"],True,(255,255,255))
            self.screen.blit(label,label.get_rect(center=rect.center))

    def render_score(self, score_state):
        label = self.font.render(f"{self.config['ui_config']['score_label']}: {score_state.get('total_score',0)}",True,(255,255,255))
        y_pos = self.config["ui_config"]["grid_height"]*self.config["ui_config"]["cell_size"]+self.config["ui_config"]["button_height"]+10
        self.screen.blit(label,(10,y_pos))

    def handle_click(self, pos):
        for btn in self.buttons:
            rect = pygame.Rect(btn["pos"], (80,self.config["ui_config"]["button_height"]))
            if rect.collidepoint(pos):
                print(f"[UI] Button clicked: {btn['id']}")
                if self.bus:
                    event = {"event":"button_press","source":"ui","button_id":btn["id"],"timestamp":time.time()}
                    self.bus.publish("button_press","ui",event)
                return btn["id"]
        return None

ui = UIHeadless()

def handler(command, params):
    if command == "init_ui":
        ui.initialize(params["config"])
        return json.dumps({"status":"initialized"})
    elif command == "render_board":
        ui.render_board(params["board_state"],params.get("score_state"))
        return json.dumps({"status":"rendered"})
    return json.dumps({"error":"unknown command"})
