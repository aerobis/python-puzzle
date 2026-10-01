from abc import ABC, abstractmethod
import random
import numpy as np

#Swaps, rotates and flips per grid size. Totals are 6/12/20.

SCRAMBLE_PLAN = {3: (2, 2, 2), 4: (4, 4, 4), 5: (5, 8, 7)};