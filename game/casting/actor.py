"""
file: actor.py
author: authors of rfk, modified by Jerry Lane
purpose: This class represents the actors that will appear on the game screen.
"""
# import global values and Point
import globals
from game.shared.point import Point

# class declaration
class Actor:
    """A visible, moveable thing that participates in the game. 
    
    The responsibility of Actor is to keep track of its appearance, position and velocity in 2d 
    space.

    Attributes:
        _text (string): The text to display
        _font_size (int): The font size to use.
        _color (Color): The color of the text.
        _position (Point): The screen coordinates.
        _velocity (Point): The speed and direction.
    """

    # default constructor
    def __init__(self):
        """Constructs a new Actor.
        
        Args:
            none
            
        Returns:
            nothing
        """
        self._text = ""
        self._font_size = globals.CELL_SIZE
        self._color = globals.WHITE
        self._position = Point(0, 0)
        self._velocity = Point(0, 0)

    # method to return actor's color
    def get_color(self):
        """Gets the actor's color as a tuple of three ints (r, g, b).
        
        Args:
            none
        
        Returns:
            Color: The actor's text color.
        """
        return self._color

    # method to return actor's font_size
    def get_font_size(self):
        """Gets the actor's font size.
        
        Args:
            none
        
        Returns:
            Point: The actor's font size.
        """
        return self._font_size

    # method to return actor's position
    def get_position(self):
        """Gets the actor's position in 2d space.
        
        Args:
            none
        
        Returns:
            Point: The actor's position in 2d space.
        """
        return self._position
    
    # method to return actor's char text
    def get_text(self):
        """Gets the actor's textual representation.
        
        Args:
            none
        
        Returns:
            string: The actor's textual representation.
        """
        return self._text

    # method to return actor's velocity
    def get_velocity(self):
        """Gets the actor's speed and direction.
        
        Args:
            none

        Returns:
            Point: The actor's speed and direction.
        """
        return self._velocity
    
    # method to move actor
    def move_next(self, max_x, max_y):
        """Moves the actor to its next position according to its velocity. Will wrap the position 
        from one side of the screen to the other when it reaches the given maximum x and y values.
        
        Args:
            max_x (int): The maximum x value.
            max_y (int): The maximum y value.

        Returns:
            nothing
        """
        x = (self._position.get_x() + self._velocity.get_x()) % max_x
        y = (self._position.get_y() + self._velocity.get_y()) % max_y
        self._position = Point(x, y)

    # method to set actor's color
    def set_color(self, color):
        """Updates the color to the given one.
        
        Args:
            color (Color): The given color.

        Returns: 
            nothing
        """
        self._color = color

    # method to set actor's position
    def set_position(self, position):
        """Updates the position to the given one.
        
        Args:
            position (Point): The given position.

        Returns: 
            nothing
        """
        self._position = position
    
    # method to set actor's font size
    def set_font_size(self, font_size):
        """Updates the font size to the given one.
        
        Args:
            font_size (int): The given font size.

        Returns:
            nothing
        """
        self._font_size = font_size
    
    # method to set a char as text
    def set_text(self, text):
        """Updates the text to the given value.
        
        Args:
            text (char): The given value.

        Returns: 
            nothing
        """
        self._text = text

    # method to set the actor's velocity
    def set_velocity(self, velocity):
        """Updates the velocity to the given one.
        
        Args:
            velocity (Point): The given velocity.

        Returns:
            nothing
        """
        self._velocity = velocity