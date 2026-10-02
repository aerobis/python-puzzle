"""
HIT137 Assignment 3
Image Puzzle Game

Shared entry point for the group project.

Current integration:
- Image processing
- Puzzle / OOP game logic

Still to integrate:
- Tkinter GUI
- Gameplay, difficulty and scoring
"""

from image_processor import ImageProcessor
from puzzle import Puzzle


# ---------------------------------------------------------
# PART 3 - TKINTER GUI
# Molly
# ---------------------------------------------------------
#
# Molly's final GUI will be imported here after her branch
# has been reviewed and merged.
#
# Expected final import:
#
# from gui import PuzzleGUI
#
# ---------------------------------------------------------


# ---------------------------------------------------------
# PART 4 - GAMEPLAY
# Himanshu
# ---------------------------------------------------------
#
# GameplayManager is still being developed separately.
# It will be imported after the GUI is ready and final
# integration has been tested.
#
# Expected final import:
#
# from gameplay import GameplayManager
#
# ---------------------------------------------------------


def create_puzzle(image_path, grid_size):
    """
    Load an image and create the puzzle model.

    ImageProcessor handles the image data.
    Puzzle handles the game state and scrambling.
    """

    processor = ImageProcessor(
        image_path=image_path,
        grid_size=grid_size
    )

    tile_images = processor.get_tile_images()

    puzzle = Puzzle(
        tile_images=tile_images,
        grid_size=grid_size
    )

    return processor, puzzle


def get_puzzle_image(puzzle):
    """
    Assemble the current Puzzle tile state into one image.
    """

    tile_images = []

    for tile in puzzle.tiles:
        tile_images.append(tile.image)

    return ImageProcessor.assemble(
        tile_images,
        puzzle.grid_size
    )


def main():
    """
    Final application entry point.

    The Tkinter GUI will start from here after Molly's
    component and GameplayManager are integrated.
    """

    print("Image Puzzle Game")
    print("-----------------")

    print("ImageProcessor: ready")
    print("Puzzle logic: ready")

    print("Tkinter GUI: waiting for integration")
    print("GameplayManager: waiting for integration")


if __name__ == "__main__":
    main()