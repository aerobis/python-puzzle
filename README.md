# HIT137 Assignment 3: Image Puzzle Game
A Tkinter desktop puzzle solving game. A loaded image is cut into a grid of tiles, scrambled with swaps, rotations and flips, and the player restores it. OpenCV handles the image processing.

## Setup
Python 3.10+ is required (Tested on Python 3.14). Tkinter ships with Python. However, on Debian/Ubuntu/WSL, it needs `sudo apt install python3-tk`.

    python -m venv .venv
    source .venv/bin/activate # For Windows, .venv\Scripts\activate 
    pip install -r requirements.txt

## Run
    
    python main.py

## How to play 101

- Pick a grid size (3x3, 4x4, 5x5) and a difficulty (Easy, Medium, Hard), then load a JPG, BMP or PNG.
- Left-click a tile to select it. Left-click another tile to swap the previous tile with that one.
- Right-click to rotate a tile 90 degrees clockwise (Mac: Control + click)
- Hint (Max 3 per image). Circles one wrong tile and it's home position. 
- Solve restores the original image.
- Green tick marks indicate that the tile is in the right place with the right orientation.

# Difficulty
- Easy: no limits, scored by moves
- Medium: countdown timer (2 / 4 / 7 minutes for 3x3 / 4x4 / 5x5), scored by time then moves
- Hard: limited moves (minimum solve cost plus an allowance) and a countdown timer. Tiles Left is hidden

# Controls
- Left click: select a tile, then click another to swap. Click the same tile to deselect
- Right click: rotate 90 degrees clockwise
- Shift + left click: flip horizontally
- Hint (max 3 per image), Solve, Restart, Hide/Show Original

## Files

- `main.py`: entry point
- `gui.py`: Tkinter interface (PuzzleGUI)
- `puzzle.py`: main game logic (Tile, Transformation, Swap, Rotate, Flip, Puzzle)
- `image_processor.py`: OpenCV, loading, resizing, tiling (ImageProcessor)
- `gameplay.py`: moves, hints, difficulty rules (GameplayManager)
- `scoreboard.py`: saves and loads scores in `scores.json`
- `test_puzzle.py` & `integration_check.py`: tests

## Tests

    python test_puzzle.py
    python integration_check.py path/to/image.jpg # Please heed specifics with host OS

# Team Information

# HIT 137: SOFTWARE NOW
## GROUP MEMBERS:
### Himanshu Bhattarai      :       S407972
### Waraphorn Boonprawat    :       S402989
### Sobit Paudel            :       S403784
### Shreyash Upreti         :       S406921

