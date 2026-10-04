"""
HIT137 Assignment 3
Part 4 - Gameplay, Moves and Score

Handles the gameplay state, difficulty rules, hints,
completion checking and scoreboard results.

This class works with the Puzzle class in puzzle.py.
"""

import json
import os
import time


class GameplayManager:

    def __init__(self, difficulty="Easy", grid_size=3):
        # Basic game state
        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False
        self.auto_solved = False

        # Difficulty information
        self.difficulty = difficulty
        self.grid_size = grid_size

        # Medium mode
        self.start_time = None
        self.time_limit = None

        # Hard mode
        self.move_limit = None

        # Local score file
        self.score_file = "scores.json"

        self.setup_difficulty()

    # -----------------------------------------------------
    # DIFFICULTY
    # -----------------------------------------------------

    def setup_difficulty(self):
        """Set the rules for the selected difficulty."""

        if self.difficulty == "Easy":
            # Easy has no timer or move restriction.
            self.time_limit = None
            self.move_limit = None
            self.start_time = None

        elif self.difficulty == "Medium":
            # Bigger puzzles receive more time.
            time_limits = {
                3: 120,
                4: 240,
                5: 420
            }

            self.time_limit = time_limits.get(self.grid_size, 120)
            self.move_limit = None
            self.start_time = time.time()

        elif self.difficulty == "Hard":
            # These are fallback limits.
            # The real limit is updated from puzzle.par_moves
            # after the puzzle has been created.
            fallback_limits = {
                3: 20,
                4: 35,
                5: 55
            }

            self.move_limit = fallback_limits.get(self.grid_size, 20)
            self.time_limit = None
            self.start_time = None

        else:
            # Invalid difficulty falls back to Easy.
            self.difficulty = "Easy"
            self.time_limit = None
            self.move_limit = None
            self.start_time = None

    def configure_puzzle(self, puzzle):
        """
        Connect difficulty settings to a newly created Puzzle.

        Hard mode uses the puzzle's calculated restoration cost
        as the starting point for its move allowance.
        """

        if self.difficulty == "Hard":
            self.set_hard_move_limit(puzzle.par_moves)

    def set_hard_move_limit(self, par_moves):
        """
        Set the Hard mode move allowance using puzzle.par_moves.

        A small allowance is added so the player does not need
        to reproduce the exact scramble reversal.
        """

        if self.difficulty != "Hard":
            return

        extra_moves = {
            3: 8,
            4: 12,
            5: 18
        }

        allowance = extra_moves.get(self.grid_size, 8)

        self.move_limit = par_moves + allowance

    # -----------------------------------------------------
    # GAME STATE
    # -----------------------------------------------------

    def reset_game(self):
        """Reset gameplay information for a new puzzle."""

        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False
        self.auto_solved = False

        self.setup_difficulty()

    def select_tile(self, tile_index):
        """
        Select a tile.

        Clicking the currently selected tile again deselects it.
        """

        if not self.can_make_move():
            return None

        if self.selected_tile == tile_index:
            self.selected_tile = None
            return None

        self.selected_tile = tile_index

        return self.selected_tile

    def add_move(self):
        """Count one valid player action."""

        if self.game_finished:
            return self.moves

        self.moves += 1

        return self.moves

    def can_make_move(self):
        """Return True when the player is allowed to make a move."""

        if self.game_finished:
            return False

        if self.difficulty == "Medium" and self.time_is_up():
            return False

        if self.difficulty == "Hard" and self.moves_are_up():
            return False

        return True

    # -----------------------------------------------------
    # PLAYER ACTIONS
    # -----------------------------------------------------

    def handle_swap(self, puzzle, first_index, second_index):
        """Swap two different tiles and count one move."""

        if not self.can_make_move():
            return False

        # Selecting the same tile twice should deselect it,
        # not count as a puzzle move.
        if first_index == second_index:
            self.selected_tile = None
            return False

        puzzle.swap(first_index, second_index)

        self.add_move()
        self.selected_tile = None

        self.check_puzzle_complete(puzzle)

        return True

    def handle_rotate(self, puzzle, tile_index):
        """Rotate a tile clockwise and count one move."""

        if not self.can_make_move():
            return False

        puzzle.rotate(tile_index)

        self.add_move()

        self.check_puzzle_complete(puzzle)

        return True

    def handle_flip(self, puzzle, tile_index):
        """Flip a tile horizontally and count one move."""

        if not self.can_make_move():
            return False

        puzzle.flip(tile_index)

        self.add_move()

        self.check_puzzle_complete(puzzle)

        return True

    # -----------------------------------------------------
    # HINTS
    # -----------------------------------------------------

    def get_hint(self, puzzle):
        """
        Use one hint.

        Puzzle.hint_target() returns:
            (current_position, correct_home_position)

        Returns None if no hint can be given.
        """

        if self.game_finished:
            return None

        if self.hints_left <= 0:
            return None

        hint = puzzle.hint_target()

        # The puzzle is already solved.
        if hint is None:
            return None

        self.hints_left -= 1

        return hint

    # Kept for simple GUI compatibility.
    def use_hint(self):
        """Use one hint without requesting a Puzzle target."""

        if self.game_finished:
            return False

        if self.hints_left <= 0:
            return False

        self.hints_left -= 1

        return True

    # -----------------------------------------------------
    # SOLVE AND COMPLETION
    # -----------------------------------------------------

    def solve_puzzle(self, puzzle):
        """
        Automatically restore the puzzle.

        Auto-solved games are not saved to the scoreboard.
        """

        if self.game_finished:
            return False

        puzzle.solve()

        self.auto_solved = True
        self.game_finished = True
        self.selected_tile = None

        return True

    def check_puzzle_complete(self, puzzle):
        """
        Check whether the player has correctly completed the puzzle.
        """

        if puzzle.is_solved():

            if not self.game_finished:
                self.finish_game()

            return True

        return False

    def finish_game(self):
        if self.game_finished:
            return False
        self.game_finished = True
        self.selected_tile = None
        return True

    # -----------------------------------------------------
    # TIMER AND MOVE LIMITS
    # -----------------------------------------------------

    def get_time_left(self):
        """Return remaining seconds for Medium mode."""

        if self.difficulty != "Medium":
            return None

        if self.start_time is None:
            return self.time_limit

        elapsed = int(time.time() - self.start_time)

        return max(0, self.time_limit - elapsed)

    def get_moves_left(self):
        """Return remaining moves for Hard mode."""

        if self.difficulty != "Hard":
            return None

        if self.move_limit is None:
            return None

        return max(0, self.move_limit - self.moves)

    def time_is_up(self):
        """Check whether Medium mode has run out of time."""

        if self.difficulty != "Medium":
            return False

        return self.get_time_left() <= 0

    def moves_are_up(self):
        """Check whether Hard mode has used all available moves."""

        if self.difficulty != "Hard":
            return False

        moves_left = self.get_moves_left()

        if moves_left is None:
            return False

        return moves_left <= 0

    def game_limit_reached(self):
        """Check whether the current difficulty limit is exhausted."""

        if self.difficulty == "Medium":
            return self.time_is_up()

        if self.difficulty == "Hard":
            return self.moves_are_up()

        return False

    # -----------------------------------------------------
    # PUZZLE INFORMATION FOR THE GUI
    # -----------------------------------------------------

    def get_tiles_left(self, puzzle):
        """Return the number of tiles still in an incorrect state."""

        return puzzle.incorrect_count()

    def get_moves(self):
        """Return moves made by the player."""

        return self.moves

    def get_hints_left(self):
        """Return hints still available."""

        return self.hints_left

    def get_selected_tile(self):
        """Return the currently selected tile."""

        return self.selected_tile

    # -----------------------------------------------------
    # SCOREBOARD
    # -----------------------------------------------------

    def calculate_result(self):
        """Create the scoreboard result for the current difficulty."""

        if self.difficulty == "Easy":
            return {
                "grid": self.grid_size,
                "moves": self.moves
            }

        if self.difficulty == "Medium":
            elapsed = int(time.time() - self.start_time)

            return {
                "grid": self.grid_size,
                "time": elapsed,
                "moves": self.moves
            }

        if self.difficulty == "Hard":
            return {
                "grid": self.grid_size,
                "moves_left": self.get_moves_left(),
                "moves_used": self.moves
            }

        return None

    def load_scores(self):
        """Load saved leaderboard results."""

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

            for difficulty in empty_scores:
                if difficulty not in scores:
                    scores[difficulty] = []

            return scores

        except (json.JSONDecodeError, OSError, TypeError):
            return empty_scores

    def sort_scores(self, scores):
        """Sort the leaderboard and keep five results per difficulty."""

        # Easy: fewer moves is better.
        scores["Easy"].sort(
            key=lambda result: result.get("moves", 999999)
        )

        # Medium: lower completion time is better.
        scores["Medium"].sort(
            key=lambda result: result.get("time", 999999)
        )

        # Hard: more remaining moves is better.
        scores["Hard"].sort(
            key=lambda result: result.get("moves_left", -1),
            reverse=True
        )

        scores["Easy"] = scores["Easy"][:5]
        scores["Medium"] = scores["Medium"][:5]
        scores["Hard"] = scores["Hard"][:5]

    def save_score(self):
        """Save a manually completed game to scores.json."""

        result = self.calculate_result()

        if result is None:
            return False

        scores = self.load_scores()

        scores[self.difficulty].append(result)

        self.sort_scores(scores)

        try:
            with open(self.score_file, "w", encoding="utf-8") as file:
                json.dump(scores, file, indent=4)

            return True

        except OSError:
            return False


# ---------------------------------------------------------
# BASIC LOCAL TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("GameplayManager basic test")
    print("--------------------------")

    easy_game = GameplayManager("Easy", 3)

    print("Easy difficulty:", easy_game.difficulty)
    print("Starting moves:", easy_game.get_moves())
    print("Starting hints:", easy_game.get_hints_left())

    medium_game = GameplayManager("Medium", 4)

    print("Medium time left:", medium_game.get_time_left())

    hard_game = GameplayManager("Hard", 5)

    print("Hard fallback moves:", hard_game.get_moves_left())