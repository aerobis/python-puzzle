import sys
import cv2
import numpy as np
from image_processor import ImageProcessor, BOARD_SIZE
from puzzle import Puzzle

path = sys.argv[1] # any jpg/png/bmp

# test puzzle generation, solving, and verification across multiple grid sizes

for n in (3, 4, 5):
    # initialize the image processor and split the image into an n x n grid of tiles
    proc = ImageProcessor(path, n)
    puzzle = Puzzle(proc.get_tile_images(), n)
     
     # ensure the newly created puzzle starts in an unresolved (scrambled) state
    assert not puzzle.is_solved()
     
     # reconstruct and save the scrambled image using the current tile configuration
    scrambled = ImageProcessor.assemble([t.image for t in puzzle.tiles], n)
    assert scrambled.shape == (BOARD_SIZE, BOARD_SIZE, 3), scrambled.shape
    cv2.imwrite("scrambled_%dx%d.png" % (n, n), scrambled)

    # solve the puzzle and rebuild the image from the solved tiles
    puzzle.solve()
    restored = ImageProcessor.assemble([t.image for t in puzzle.tiles], n)
    
    # verify that the puzzle is successfully solved and matches the original image
    assert puzzle.is_solved()
    assert np.array_equal(restored, proc.get_original_image())
    print(n, "x", n, "OK, par moves was", puzzle.par_moves)

print("Integration good to go")