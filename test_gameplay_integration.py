import numpy as np

from puzzle import Puzzle
from gameplay import GameplayManager


def make_test_tiles(grid_size):
    """Create simple unique image tiles for testing."""

    tiles = []

    total_tiles = grid_size * grid_size

    for i in range(total_tiles):
        tile = np.full(
            (20, 20, 3),
            i * 5,
            dtype=np.uint8
        )

        tiles.append(tile)

    return tiles


def test_gameplay(grid_size, difficulty):
    print()
    print("--------------------------------")
    print("Testing", difficulty, str(grid_size) + "x" + str(grid_size))
    print("--------------------------------")

    tiles = make_test_tiles(grid_size)

    puzzle = Puzzle(tiles, grid_size)

    game = GameplayManager(difficulty, grid_size)

    game.configure_puzzle(puzzle)

    print("Puzzle par moves:", puzzle.par_moves)
    print("Incorrect tiles:", game.get_tiles_left(puzzle))
    print("Starting moves:", game.get_moves())
    print("Hints:", game.get_hints_left())

    if difficulty == "Medium":
        print("Time left:", game.get_time_left())

    if difficulty == "Hard":
        print("Move limit:", game.move_limit)
        print("Moves left:", game.get_moves_left())

    hint = game.get_hint(puzzle)

    print("Hint:", hint)
    print("Hints remaining:", game.get_hints_left())

    game.handle_rotate(puzzle, 0)

    print("Moves after rotate:", game.get_moves())

    game.solve_puzzle(puzzle)

    print("Solved:", puzzle.is_solved())
    print("Game finished:", game.game_finished)
    print("Auto solved:", game.auto_solved)


if __name__ == "__main__":

    test_gameplay(3, "Easy")
    test_gameplay(4, "Medium")
    test_gameplay(5, "Hard")

    print()
    print("Gameplay integration test completed.")