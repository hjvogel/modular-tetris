import json

class ScoringSystem:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0

    def update_score(self, lines_cleared):
        points_per_line = {1: 100, 2: 300, 3: 500, 4: 800}
        gained_score = points_per_line.get(lines_cleared, 0) * self.level
        self.score += gained_score
        self.lines_cleared_total += lines_cleared
        self.level = self.lines_cleared_total // 10 + 1

        event = {
            "event": "score_update",
            "score": self.score,
            "lines_cleared": lines_cleared,
            "level": self.level
        }
        return json.dumps(event)

# Example usage with pygame (pseudo-integration)
# scoring = ScoringSystem()
# print(scoring.update_score(2))
# print(scoring.update_score(4))