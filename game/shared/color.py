"""
file: color.py
author: authors of rfk and Jerry Lane
purpose: This class represents the color of an object based on the red, blue, gree, and 
alpha elements of it.
"""

# class declaration
class Color:
    """A color.

    The responsibility of Color is to hold and provide information about itself. Color has a few 
    convenience methods for comparing them and converting to a tuple.

    Attributes:
        _red (int): The red value.
        _green (int): The green value.
        _blue (int): The blue value.
        _alpha (int): The alpha or opacity.
    """
    
    # default constructor
    def __init__(self, red, green, blue, alpha = 255):
        """Constructs a new Color using the specified red, green, blue and alpha values. The alpha 
        value is the color's opacity.
        
        Args:
            red (int): A red value.
            green (int): A green value.
            blue (int): A blue value.
            alpha (int): An alpha or opacity.

        Returns: 
            nothing
        """
        self._red = red
        self._green = green
        self._blue = blue 
        self._alpha = alpha

    # method to return the rgba values individually
    def to_tuple(self):
        """Gets the color as a tuple of four values (red, green, blue, alpha).

        Args:
            none
            
        Returns:
            Tuple(int, int, int, int): The color as a tuple.
        """
        return (self._red, self._green, self._blue, self._alpha)  

    # method to compare two colors
    def equals(self, other):
        """Compares the red, blue, and green components of a color. It
        returns true if all three match or false if any one of them do not.

        Args:
            other (Color): the other color to compare self against

        Returns: 
            (bool) True - if all three of the rgb values match
            (bool) False - if any of the three do not match
        """
        # break other color down into components
        other_red, other_green, other_blue, other_alpha = other.to_tuple()
        
        # compare self's red, green, and blue components to other's
        if other_red == self._red and \
           other_green == self._green and \
           other_blue == self._blue:
            
            # return true if they match
            return True
        else:

            # return false if they don't
            return False 