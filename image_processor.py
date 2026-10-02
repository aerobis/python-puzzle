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

    def split_tiles(self):
        h, w, _ = self.original_img.shape
        th = h // self.grid_size
        tw = w // self.grid_size
        
        self.tiles = []
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                tile_img = self.original_img[r*th:(r+1)*th, c*tw:(c+1)*tw].copy()
                self.tiles.append({
                    'img': tile_img,
                    'home_r': r,
                    'home_c': c,
                    'rot': 0,
                    'flipped': False
                })

    def scramble(self):
        # scale moves based on grid size rules
        if self.grid_size == 3:
            num_moves = 6
        elif self.grid_size == 4:
            num_moves = 12
        else:
            num_moves = 20

        for _ in range(num_moves):
            idx = random.randint(0, len(self.tiles) - 1)
            action = random.choice(['rot', 'flip', 'swap'])
            
            if action == 'rot':
                angle = random.choice([90, 180, 270])
                if angle == 90:
                    code = cv2.ROTATE_90_CLOCKWISE
                elif angle == 180:
                    code = cv2.ROTATE_180
                else:
                    code = cv2.ROTATE_90_COUNTERCLOCKWISE
                    
                self.tiles[idx]['img'] = cv2.rotate(self.tiles[idx]['img'], code)
                self.tiles[idx]['rot'] = (self.tiles[idx]['rot'] + angle) % 360
                
            elif action == 'flip':
                f_code = random.choice([0, 1])
                self.tiles[idx]['img'] = cv2.flip(self.tiles[idx]['img'], f_code)
                self.tiles[idx]['flipped'] = not self.tiles[idx]['flipped']
                
            elif action == 'swap':
                idx2 = random.randint(0, len(self.tiles) - 1)
                self.tiles[idx], self.tiles[idx2] = self.tiles[idx2], self.tiles[idx]

    def get_board_image(self):
        rows = []
        th, tw, _ = self.tiles[0]['img'].shape
        
        for r in range(self.grid_size):
            row_pieces = []
            for c in range(self.grid_size):
                i = r * self.grid_size + c
                piece = self.tiles[i]['img'].copy()
                # draw a faint grid border
                cv2.rectangle(piece, (0, 0), (tw-1, th-1), (200, 200, 200), 1)
                row_pieces.append(piece)
            rows.append(np.hstack(row_pieces))
            
        return np.vstack(rows)

if __name__ == "__main__":
    p = ImageProcessor('test.png', 3)
    p.scramble()
    
    # Get the scrambled board image and save it
    scrambled_img = p.get_board_image()
    cv2.imwrite('scrambled_test.png', scrambled_img)
    
    print("Done scrambling and saved as 'scrambled_test.png'!")