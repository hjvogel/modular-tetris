import json

class UIHeadless:
    def render_board(self, board_state):
        # Convert board state to JSON for frontend use
        return json.dumps({"action": "render_board", "board_state": board_state})

    def handle_ui_event(self, event_type, ui_elements):
        event = {"action": event_type, "ui_elements": ui_elements}
        return json.dumps(event)

# Example usage with pygame (pseudo-integration)
# ui = UIHeadless()
# board_state = {"width":10, "height":20, "grid":[[0]*10]*20}
# print(ui.render_board(board_state))
# print(ui.handle_ui_event("button_press", [{"type":"button", "id":"start"}]))