"""
HIT137 Assignment 3
Part 4 - Gameplay, Moves and Score

This class keeps track of the player's gameplay information
and the rules for each difficulty level.
"""

import time


class GameplayManager:

    def __init__(self, difficulty="Easy", grid_size=3):

        # Basic gameplay information
        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False

        # Difficulty settings
        self.difficulty = difficulty
        self.grid_size = grid_size

        # Medium difficulty timer
        self.start_time = None
        self.time_limit = None

        # Hard difficulty move restriction
        self.move_limit = None

        self.setup_difficulty()

    def setup_difficulty(self):
        """Set the rules depending on the selected difficulty."""

        if self.difficulty == "Easy":

            # Easy mode has no time or move restriction
            self.time_limit = None
            self.move_limit = None

        elif self.difficulty == "Medium":

            # Larger puzzles are given more time
            time_limits = {
                3: 120,
                4: 240,
                5: 420
            }

            self.time_limit = time_limits.get(self.grid_size, 120)
            self.move_limit = None
            self.start_time = time.time()

        elif self.difficulty == "Hard":

            # Temporary move limits.
            # These can be adjusted later after integration
            # with the final puzzle scrambling system.
            move_limits = {
                3: 20,
                4: 35,
                5: 55
            }

            self.move_limit = move_limits.get(self.grid_size, 20)
            self.time_limit = None

        else:
            # If an invalid difficulty is received,
            # use Easy as a safe default.
            self.difficulty = "Easy"
            self.time_limit = None
            self.move_limit = None

    def reset_game(self):
        """Reset all values when a new puzzle starts."""

        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False

        self.setup_difficulty()

    def select_tile(self, tile_index):
        """Select or deselect a puzzle tile."""

        if self.game_finished:
            return None

        if self.selected_tile == tile_index:
            self.selected_tile = None
            return None

        self.selected_tile = tile_index

        return self.selected_tile

    def add_move(self):
        """Add one move after a valid puzzle action."""

        if self.game_finished:
            return self.moves

        self.moves += 1

        return self.moves

    def use_hint(self):
        """Use one of the three available hints."""

        if self.game_finished:
            return False

        if self.hints_left <= 0:
            return False

        self.hints_left -= 1

        return True

    def get_time_left(self):
        """Return the remaining time for Medium difficulty."""

        if self.difficulty != "Medium":
            return None

        if self.start_time is None:
            return self.time_limit

        elapsed = int(time.time() - self.start_time)

        remaining = self.time_limit - elapsed

        return max(0, remaining)

    def get_moves_left(self):
        """Return the remaining moves for Hard difficulty."""

        if self.difficulty != "Hard":
            return None

        remaining = self.move_limit - self.moves

        return max(0, remaining)

    def time_is_up(self):
        """Check whether the Medium timer has expired."""

        if self.difficulty != "Medium":
            return False

        return self.get_time_left() <= 0

    def moves_are_up(self):
        """Check whether the Hard move allowance has been used."""

        if self.difficulty != "Hard":
            return False

        return self.get_moves_left() <= 0

    def finish_game(self):
        """Mark the puzzle as completed."""

        self.game_finished = True
        self.selected_tile = None

    def get_moves(self):
        """Return the number of moves used."""

        return self.moves

    def get_hints_left(self):
        """Return the number of hints remaining."""

        return self.hints_left


# Testing only
if __name__ == "__main__":

    print("----- EASY TEST -----")

    easy_game = GameplayManager("Easy", 3)

    easy_game.add_move()
    easy_game.add_move()

    print("Difficulty:", easy_game.difficulty)
    print("Moves:", easy_game.get_moves())
    print("Time limit:", easy_game.time_limit)
    print()

    print("----- MEDIUM TEST -----")

    medium_game = GameplayManager("Medium", 4)

    print("Difficulty:", medium_game.difficulty)
    print("Time left:", medium_game.get_time_left())
    print()

    print("----- HARD TEST -----")

    hard_game = GameplayManager("Hard", 3)

    hard_game.add_move()
    hard_game.add_move()

    print("Difficulty:", hard_game.difficulty)
    print("Moves used:", hard_game.get_moves())
    print("Moves left:", hard_game.get_moves_left())