"""
HIT137 Assignment 3
Image Puzzle Game

Main entry point for the completed puzzle game.
"""

from gui import PuzzleGUI


def main():
    """Start the image puzzle game."""

    app = PuzzleGUI()
    app.run()


if __name__ == "__main__":
    main()