"""
HIT137 Assignment 3
Image Puzzle Game

Shared main program for group integration.

Each group member is developing their component separately.
The imports and final program will be connected as each
component is completed and merged.
"""


# =========================================================
# GROUP COMPONENTS
# =========================================================

# PART 1 - OOP / GAME LOGIC
# Sobit's part
#
# Expected responsibilities:
# - Tile / Puzzle classes
# - swap tiles
# - rotate tiles
# - flip tiles
# - check correct tile position/orientation
# - count incorrect tiles
# - check whether puzzle is solved
#
# Final import will be added after Sobit's branch is ready.
#
# Example only:
# from puzzle import Puzzle


# ---------------------------------------------------------


# PART 2 - IMAGE PROCESSING
# Shreyas's part
#
# Expected responsibilities:
# - load JPG/JPEG/PNG/BMP images
# - resize image while maintaining aspect ratio
# - divide image into 3x3, 4x4 or 5x5 tiles
# - scramble puzzle using swap, rotate and flip
# - return images required by the GUI
#
# Final import will be confirmed after Part 2 is completed.
#
# Current repository may already contain:
# from image_processor import ImageProcessor


# ---------------------------------------------------------


# PART 3 - TKINTER GUI / DISPLAY
# Molly's part
#
# Expected responsibilities:
# - main Tkinter window
# - image selection
# - grid size selection
# - difficulty selection
# - original image display
# - puzzle image display
# - counters / game information
# - Hint and Solve buttons
#
# Final import will be added after Molly's branch is ready.
#
# Example only:
# from gui import PuzzleGUI


# ---------------------------------------------------------


# PART 4 - GAMEPLAY / MOVES / SCORE
# Himanshu's part
#
# Currently being developed separately.
#
# Responsibilities:
# - move tracking
# - tile selection state
# - maximum 3 hints
# - completion handling
# - Easy / Medium / Hard rules
# - Medium countdown timer
# - Hard move allowance
# - difficulty-based scoring
# - scoreboard saving
#
# This part will be integrated after Parts 1-3 provide
# their final classes and methods.
#
# Final import:
# from gameplay import GameplayManager


# =========================================================
# FINAL PROGRAM
# =========================================================

def main():
    """
    Start the final image puzzle game.

    The completed group components will be connected here
    after each member finishes their branch.
    """

    print("Image Puzzle Game")
    print("-----------------")
    print("Group components are currently being developed.")
    print("Run the completed GUI after final integration.")

    # -----------------------------------------------------
    # FINAL INTEGRATION FLOW
    # -----------------------------------------------------
    #
    # 1. Start Tkinter GUI.
    #
    # 2. Player selects:
    #       - image
    #       - grid size (3x3, 4x4 or 5x5)
    #       - difficulty (Easy, Medium or Hard)
    #
    # 3. ImageProcessor loads and prepares the image.
    #
    # 4. Puzzle/game logic stores the tile state and
    #    performs swap, rotate and flip operations.
    #
    # 5. GameplayManager tracks moves, hints, difficulty,
    #    timer, completion and scores.
    #
    # 6. Tkinter GUI displays all changes to the player.
    #
    # 7. When all tiles are correct, the game ends and
    #    the result is recorded.
    #
    # -----------------------------------------------------


if __name__ == "__main__":
    main()