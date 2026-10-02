import cv2
import numpy as np
import random

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")
BOARD_SIZE = 480 #So it's divisible by 3, 5 and 5, meaning every grid will be split into exact squares

class ImageProcessor:
    def __init__(self, image_path, grid_size=3):
        self.image_path = image_path
        self.grid_size = grid_size
        self.original_img = None
        self.load_image()

    def load_image(self):
        ext = os.path.splittext(self.image_path)[1].lower() #Standardize text to check extensions
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported file type: " + ext)
        
        #fromfile + imdecode also work for paths with special characters 
        data = np.fromfile(self.image_path, dtype = np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not read image: " + self.image_path)
        
        #resize keeping aspect ratio (shorter side will be BOARD_SIZE),
        #and then center crop to a square
        h, w = img.shape[:2]
        scale = BOARD_SIZE / min(h, w)
        new_w = max(BOARD_SIZE, round (w * scale))
        new_h = max(BOARD_SIZE, round(h * scale))
        interp = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
        resized = cv2.resize(img, (new_w, new_h), interpolation=interp)
        
        top = (new_h - BOARD_SIZE) // 2
        left = (new_w - BOARD_SIZE) // 2
        self.original_img = resized[top: top + BOARD_SIZE, left: left + BOARD_SIZE].copy()

    def get_original_image(self):
        return self.original_image.copy()
    
    def get_tile_images(self):
        #unscrambled tiles, row by row. pass these to Puzzle(tiles, grid_size)
        n = self.grid_size
        side = BOARD_SIZE // n
        tiles = []
        for r in range(n):
            for c in range(n):
                piece = self.original_img[r * side:(r + 1) * side, c * side: (c + 1) * side]
                tiles.append(piece.copy())
        
        return tiles
    
    

    