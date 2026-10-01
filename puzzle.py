from abc import ABC, abstractmethod
import random
import numpy as np

#Swaps, rotates and flips per grid size. Totals are 6/12/20.

SCRAMBLE_PLAN = {3: (2, 2, 2), 4: (4, 4, 4), 5: (5, 8, 7)};

class Title:
    def __init__(self, image, home_index):
        self._original = image
        self._image = image.copy()
        self._home_index = home_index
        
    @property
    def image(self):
        return self._image
    
    @property
    def home_index(self):
        return self._home_index
    
    def rotate(self, quarter_turns):
        self._image = np.rot90(self._image, -quarter_turns).copy()
    
    def flip(self, horizontal):
        if horizontal:
            flipped = np.fliplr(self._image)
        else:
            flipped = np.flipud(self._image)
        self._image = flipped.copy();
        
    def is_upright(self):
        return np.array_equal(self._image, self._original)
    
