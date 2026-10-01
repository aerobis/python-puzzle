"""
HIT137 Assignment 3
Part 4 - Gameplay, Moves and Score

Handles gameplay state, difficulty rules and score saving.
"""

import time
import json
import os


class GameplayManager:

    def __init__(self, difficulty="Easy", grid_size=3):

        # Basic gameplay information
        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False

        # Difficulty information
        self.difficulty = difficulty
        self.grid_size = grid_size

        # Medium timer
        self.start_time = None
        self.time_limit = None

        # Hard move restriction
        self.move_limit = None

        # File used to save completed scores
        self.score_file = "scores.json"

        self.setup_difficulty()

    def setup_difficulty(self):
        """Set the rules for the selected difficulty."""

        if self.difficulty == "Easy":

            self.time_limit = None
            self.move_limit = None

        elif self.difficulty == "Medium":

            time_limits = {
                3: 120,
                4: 240,
                5: 420
            }

            self.time_limit = time_limits.get(self.grid_size, 120)
            self.move_limit = None
            self.start_time = time.time()

        elif self.difficulty == "Hard":

            move_limits = {
                3: 20,
                4: 35,
                5: 55
            }

            self.move_limit = move_limits.get(self.grid_size, 20)
            self.time_limit = None

        else:

            self.difficulty = "Easy"
            self.time_limit = None
            self.move_limit = None

    def reset_game(self):
        """Reset gameplay values for a new puzzle."""

        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False

        self.setup_difficulty()

    def select_tile(self, tile_index):
        """Select a tile or deselect it when clicked again."""

        if self.game_finished:
            return None

        if self.selected_tile == tile_index:
            self.selected_tile = None
            return None

        self.selected_tile = tile_index

        return self.selected_tile

    def add_move(self):
        """Count one valid puzzle action."""

        if self.game_finished:
            return self.moves

        self.moves += 1

        return self.moves

    def use_hint(self):
        """Use one hint if one is available."""

        if self.game_finished:
            return False

        if self.hints_left <= 0:
            return False

        self.hints_left -= 1

        return True

    def get_time_left(self):
        """Return remaining Medium difficulty time."""

        if self.difficulty != "Medium":
            return None

        elapsed = int(time.time() - self.start_time)

        return max(0, self.time_limit - elapsed)

    def get_moves_left(self):
        """Return remaining Hard difficulty moves."""

        if self.difficulty != "Hard":
            return None

        return max(0, self.move_limit - self.moves)

    def time_is_up(self):
        """Return True when Medium mode has run out of time."""

        if self.difficulty != "Medium":
            return False

        return self.get_time_left() <= 0

    def moves_are_up(self):
        """Return True when Hard mode has no moves remaining."""

        if self.difficulty != "Hard":
            return False

        return self.get_moves_left() <= 0

    def calculate_result(self):
        """Create a score based on the current difficulty."""

        if self.difficulty == "Easy":

            return {
                "grid": self.grid_size,
                "moves": self.moves
            }

        elif self.difficulty == "Medium":

            elapsed = int(time.time() - self.start_time)

            return {
                "grid": self.grid_size,
                "time": elapsed,
                "moves": self.moves
            }

        elif self.difficulty == "Hard":

            return {
                "grid": self.grid_size,
                "moves_left": self.get_moves_left(),
                "moves_used": self.moves
            }

    def load_scores(self):
        """Load previous scores from scores.json."""

        empty_scores = {
            "Easy": [],
            "Medium": [],
            "Hard": []
        }

        if not os.path.exists(self.score_file):
            return empty_scores

        try:

            with open(self.score_file, "r", encoding="utf-8") as file:
                scores = json.load(file)

            # Make sure all three difficulty lists exist
            for difficulty in empty_scores:

                if difficulty not in scores:
                    scores[difficulty] = []

            return scores

        except (json.JSONDecodeError, OSError):

            return empty_scores

    def sort_scores(self, scores):
        """Sort and keep the five best scores for each difficulty."""

        # Easy: fewer moves is better
        scores["Easy"].sort(
            key=lambda result: result.get("moves", 999999)
        )

        # Medium: less time is better
        scores["Medium"].sort(
            key=lambda result: result.get("time", 999999)
        )

        # Hard: more remaining moves is better
        scores["Hard"].sort(
            key=lambda result: result.get("moves_left", -1),
            reverse=True
        )

        scores["Easy"] = scores["Easy"][:5]
        scores["Medium"] = scores["Medium"][:5]
        scores["Hard"] = scores["Hard"][:5]

    def save_score(self):
        """Save the current completed result."""

        scores = self.load_scores()

        result = self.calculate_result()

        scores[self.difficulty].append(result)

        self.sort_scores(scores)

        try:

            with open(self.score_file, "w", encoding="utf-8") as file:
                json.dump(scores, file, indent=4)

            return True

        except OSError:

            return False

    def finish_game(self):
        """Finish the puzzle and save the result."""

        # Prevent the same completed puzzle being saved twice
        if self.game_finished:
            return False

        self.game_finished = True
        self.selected_tile = None

        self.save_score()

        return True

    def get_moves(self):
        return self.moves

    def get_hints_left(self):
        return self.hints_left


# Testing only
if __name__ == "__main__":

    game = GameplayManager("Easy", 3)

    game.add_move()
    game.add_move()
    game.add_move()

    print("Moves before finishing:", game.get_moves())

    game.finish_game()

    print("Game finished:", game.game_finished)
    print("Score saved to scores.json")