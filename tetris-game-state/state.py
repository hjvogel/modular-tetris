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
            "source": "tetris-game-state",
            "timestamp": datetime.utcnow().isoformat() + "Z",
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

# -- Singleton instance --
game_state = GameState()

# -- Plugin-compatible handler --
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