"""
file: globals.py
author: Jerry Lane
purpose: This file holds global values used throughout the program.
"""
# import os to make sense of the DATA_PATH and Color for statements below
import os
from game.shared.color import Color

# global values
FRAME_RATE = 12
MAX_X = 900
MAX_Y = 615
CELL_SIZE = 15
FONT_SIZE = 15
COLS = 60
ROWS = 40
CAPTION = "Battle Ships"
DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/data/messages.txt"
WHITE = Color(255, 255, 255, 255)
YELLOW = Color(255, 255, 0, 255)
GREEN = Color(0, 255, 0, 255)
RED = Color(255, 0, 0, 0)
RED_BOLD = Color(255, 0, 0, 255)
DEFAULT_ARTIFACTS = 40