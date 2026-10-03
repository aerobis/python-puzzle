import json
import os
from datetime import datetime


class Scoreboard:
    def __init__(self, filename="scores.json"):
        self.filename = filename

    def load_scores(self):
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (json.JSONDecodeError, OSError):
            pass

        return []

    def save_score(self, difficulty, grid_size, result):
        scores = self.load_scores()

        score = {
            "difficulty": difficulty,
            "grid_size": grid_size,
            "result": result,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        scores.append(score)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(scores, file, indent=4)

    def get_scores(self, difficulty=None):
        scores = self.load_scores()

        if difficulty is not None:
            scores = [
                score for score in scores
                if score["difficulty"] == difficulty
            ]

        return scores