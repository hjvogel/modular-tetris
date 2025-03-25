import json

LINE_SCORES = {
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}

score_state = {
    "lines_cleared": 0,
    "total_score": 0,
    "level": 1
}

def update_score(lines):
    score_gain = LINE_SCORES.get(lines, 0)
    score_state["lines_cleared"] += lines
    score_state["total_score"] += score_gain
    return score_state

def reset_score():
    score_state["lines_cleared"] = 0
    score_state["total_score"] = 0
    score_state["level"] = 1
    return score_state

def handler(command, params):
    if command == "update_score":
        lines = params.get("lines", 0)
        updated = update_score(lines)
        return json.dumps({
            "event": "score_update",
            "source": "tetris-scoring-rules",
            "payload": updated
        })
    elif command == "get_score":
        return json.dumps(score_state)
    elif command == "reset_score":
        reset = reset_score()
        return json.dumps({
            "event": "score_reset",
            "source": "tetris-scoring-rules",
            "payload": reset
        })
    return json.dumps({
        "error": "Unknown scoring command",
        "received": command
    })