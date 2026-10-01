"""
HIT137 Assignment 3
Part 4 - Gameplay, Moves and Score

This class keeps track of the player's gameplay information.
"""


class GameplayManager:

    def __init__(self):
        # Number of moves made by the player
        self.moves = 0

        # Assignment allows a maximum of 3 hints
        self.hints_left = 3

        # Stores the tile currently selected by the player
        self.selected_tile = None

        # Used to stop actions after the puzzle is completed
        self.game_finished = False

    def reset_game(self):
        """Reset all gameplay values for a new puzzle."""

        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False

    def select_tile(self, tile_index):
        """Select or deselect a puzzle tile."""

        if self.game_finished:
            return None

        # Clicking the selected tile again deselects it
        if self.selected_tile == tile_index:
            self.selected_tile = None
            return None

        self.selected_tile = tile_index

        return self.selected_tile

    def add_move(self):
        """Add one move after a valid swap, rotation or flip."""

        if self.game_finished:
            return self.moves

        self.moves += 1

        return self.moves

    def use_hint(self):
        """Use one hint if the player still has hints available."""

        if self.game_finished:
            return False

        if self.hints_left <= 0:
            return False

        self.hints_left -= 1

        return True

    def finish_game(self):
        """Mark the puzzle as completed and stop further input."""

        self.game_finished = True
        self.selected_tile = None

    def get_moves(self):
        """Return the current move count."""

        return self.moves

    def get_hints_left(self):
        """Return the number of hints remaining."""

        return self.hints_left


# This section is only for testing this file by itself
if __name__ == "__main__":

    game = GameplayManager()

    print("Starting moves:", game.get_moves())
    print("Starting hints:", game.get_hints_left())

    game.select_tile(2)

    print("Selected tile:", game.selected_tile)

    game.add_move()

    print("Moves after one action:", game.get_moves())

    game.use_hint()

    print("Hints after one hint:", game.get_hints_left())