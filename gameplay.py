"""
HIT137 Assignment 3
Part 4 - Puzzle Gameplay, Moves and Score

This file handles the gameplay state.
The GUI will call these methods when the player makes a move.
"""


class GameplayManager:

    def __init__(self):
        # Basic round information
        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False

    def reset_game(self):
        """Reset the gameplay values for a new puzzle."""

        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.game_finished = False

    def select_tile(self, tile_index):
        """
        Store the first tile selected by the player.

        If the same tile is clicked again, it is deselected.
        """

        if self.game_finished:
            return None

        if self.selected_tile == tile_index:
            self.selected_tile = None
            return None

        self.selected_tile = tile_index
        return tile_index

    def add_move(self):
        """Increase the move counter after a valid puzzle action."""

        if not self.game_finished:
            self.moves += 1

        return self.moves

    def use_hint(self):
        """
        Use one of the three available hints.

        Returns True if a hint can be used.
        Returns False when no hints remain.
        """

        if self.game_finished:
            return False

        if self.hints_left <= 0:
            return False

        self.hints_left -= 1
        return True

    def finish_game(self):
        """Lock the current puzzle when it has been completed."""

        self.game_finished = True
        self.selected_tile = None

    def get_moves(self):
        return self.moves

    def get_hints_left(self):
        return self.hints_left


if __name__ == "__main__":
    # Small test for this file only.
    game = GameplayManager()

    print("Moves:", game.get_moves())
    print("Hints:", game.get_hints_left())

    game.select_tile(2)
    print("Selected tile:", game.selected_tile)

    game.add_move()
    print("Moves after action:", game.get_moves())

    game.use_hint()
    print("Hints after using one:", game.get_hints_left())