"""
file: keyboard_service.py
author: authors of rfk and Jerry Lane
purpose: This class represents the keyboard input functions in the game.
"""
# import pyray for input function and Point to track changes
import pyray
from game.shared.point import Point

# class declaration
class KeyboardService:
    """Detects player input. 
    
    The responsibility of a KeyboardService is to detect player key presses and translate them into 
    a point representing a direction.

    Attributes:
        cell_size (int): For scaling directional input to a grid.
        enter_key_up (bool): For checking Enter key up
        enter_key_down (bool): For checking Enter key down
    """

    # default constructor
    def __init__(self, cell_size = 1):
        """Constructs a new KeyboardService using the specified cell size.
        
        Args:
            cell_size (int): The size of a cell in the display grid.

        Returns:
            nothing
        """
        self._cell_size = cell_size
        self._enter_key_up = False
        self._enter_key_down = False

    # method to return the direction based on cursor key pressed
    def get_direction(self):
        """Gets the selected direction based on the currently pressed keys.

        Args:
            none

        Returns:
            Point: The selected direction.
        """
        # clear x and y values
        dx = 0
        dy = 0

        # change x and y values depending on keys pressed
        if pyray.is_key_down(pyray.KEY_LEFT):
            dx = -1
        
        if pyray.is_key_down(pyray.KEY_RIGHT):
            dx = 1
        
        if pyray.is_key_down(pyray.KEY_UP):
            dy = -1
        
        if pyray.is_key_down(pyray.KEY_DOWN):
            dy = 1

        # set direction change, if any, in a Point, scale it to the grid, and return
        direction = Point(dx, dy)
        direction = direction.scale(self._cell_size)
        return direction

    # method to read the Enter key
    def get_enter_key_state(self):
        """Gets the state of the Enter key and returns it.

        Args:
            none

        Return:
            (bool) True if Enter key is pressed
            (bool) False if Enter key is up
        """
        # set initial state of Enter key
        self._enter_key_down = False

        # if Enter key is pressed, set flag and return
        if pyray.is_key_down(pyray.KEY_ENTER):
            self._enter_key_down = True
        return self._enter_key_down

    # method to check if the Enter key is up
    def is_enter_key_up(self):
        """Gets the state of the Enter key and returns it.

        Args:
            none

        Return:
            (bool) True if Enter key is up
            (bool) False if Enter key is pressed
        """
        # set initial state of Enter key
        self._enter_key_up = False

        # if Enter key is up, set flag and return
        if pyray.is_key_up(pyray.KEY_ENTER):
            self._enter_key_up = True
        return self._enter_key_up
        