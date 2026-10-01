from abc import ABC, abstractmethod
import random
import numpy as np

#Swaps, rotates and flips per grid size. Totals are 6/12/20.

SCRAMBLE_PLAN = {3: (2, 2, 2), 4: (4, 4, 4), 5: (5, 8, 7)};

class Tile:
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
    
class Transformation(ABC):
    @abstractmethod
    def apply(self, puzzle):
        pass
    
    @abstractmethod
    def undo(self, puzzle):
        pass
    
    @property
    @abstractmethod
    def restore_cost(self, puzzle):
        pass
    
class Swap(Transformation):
    def __init__(self, i, j):
        self.i = i
        self.j = j
    
    def apply(self, puzzle):
        puzzle.swap_tiles(self. i, self, j)
        
    def undo(self, puzzle):
        puzzle.swap_tiles(self.i, self.j)
        
    @property
    def restore_cost(self):
        return 1
    
class Rotate(Transformation):
    def __init__(self, index, quarter_turns = 1):
        self.index = index
        self.turns = quarter_turns
        
    def apply(self, puzzle):
        puzzle.tiles[self.index].rotate(self.turns)
        
    def undo(self, puzzle):
        puzzle.tiles[self.index].rotate(-self.turns)
    
    @property
    def restore_cost(self):
        return (4 - self.turns % 4) % 4 #Assuming a 4-tile cycle
    
class Flip(Transformation):
    def __init__(self, index, horizontal=True):
        self.index = index
        self.horizontal = horizontal

    def apply(self, puzzle):
        puzzle.tiles[self.index].flip(self.horizontal)

    def undo(self, puzzle):
        puzzle.tiles[self.index].flip(self.horizontal)

    @property
    def restore_cost(self):
        # the player can only flip horizontally, so a vertical flip
        # takes 1 flip + 2 rotations to undo
        return 1 if self.horizontal else 3
    

# SCRAMBLING
def make_scramble_plan(grid_size):
    swaps, rots, flips = SCRAMBLE_PLAN[grid_size]
    n = grid_size * grid_size
    
    # Each swap consumes 2 unique indices; each rotate/flip consumes 1
    pool = random.sample(range(n), 2 * swaps + rots + flips)   # all unique

    # First 2*swaps indices are paired up into Swap operations.
    plan = [Swap(pool[2 * k], pool[2 * k + 1]) for k in range(swaps)]

    # next 'rots' become Rotate (random quarter-turn direction 1-3)
    # last 'flips' become Flip (on a random axis) 
    rest = pool[2 * swaps:]
    plan += [Rotate(i, random.choice([1, 2, 3])) for i in rest[:rots]]
    plan += [Flip(i, random.choice([True, False])) for i in rest[rots:]]

    #Shuffle so the player can't predict which type comes first
    random.shuffle(plan)
    return plan


