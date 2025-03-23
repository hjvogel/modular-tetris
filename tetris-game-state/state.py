import json
from datetime import datetime

class GameState:
    def __init__(self):
        self.state = "initialized"
        self.details = {}

    def set_state(self, state, details=None):
        self.state = state
        self.details = details or {}
        event = {
            "event": "state_change",
            "state": self.state,
            "details": self.details
        }
        return json.dumps(event)

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

# Example usage with pygame (pseudo-integration)
# game_state = GameState()
# print(game_state.game_start())
# print(game_state.pause_game())
# print(game_state.resume_game())
# print(game_state.game_over("collision_top", 1350, 4))