"""
File: ship.py
Author: Jerry Lane
Purpose: The Ship class holds the infomation on an Actor that is
also a ship.
"""
# import global and random modules
import globals
import random

# import Actor, Point, and Color
from game.casting.actor import Actor
from game.shared.point import Point
from game.shared.color import Color

# class declaration
class Ship(Actor):
    """
    Parameters: none
    Return: nothing
    The Ship class holds the description of the ship actor in its 
    member 'message,' color components, and the cast
    """

    # constructor method for Ship
    def __init__(self, cast, color):
        """
        Parameters: none
        Return: nothing
        The constructor method merely sets the cast in an internal variable,
        sets the internal message, and stores the color. It overrides the 
        set_color() parent method.
        """
        # inherit the constructor elements of the Actor class
        super().__init__()

        # initialize attributes
        self._text = ""
        self._red, self._green, self._blue, self._alpha = color.to_tuple()
        self._cast = cast

    # method to scatter return fire
    def target(self):
        """This method fires a shot at a random point in defender territory
        
        parameters: none
        return: nothing
        """
        # set area boundaries
        x_left = globals.CELL_SIZE
        x_right = globals.MAX_X
        y_bottom = globals.MAX_Y - globals.CELL_SIZE
        y_top = int(y_bottom / 2) + globals.CELL_SIZE

        # get random target point
        x = int((random.randint(x_left, x_right)) / globals.CELL_SIZE)
        y = int(random.randint(y_top, y_bottom - globals.CELL_SIZE) / globals.CELL_SIZE)
        position = Point(x, y).scale(globals.CELL_SIZE)
        
        # check to see if it hit
        self._check_for_hit(position)

    # method to check to see if enemy hit a defender
    def _check_for_hit(self, position):
        """This method checks to see if the enemy has hit a defender with
        its random shot.
        parameters: position (Point) - a location on defense side of screen
        returns: nothing
        """
        # get defense fleet information
        defenders = self._cast.get_actors("defense_ships")

        # loop position against positions of all defenders
        for defender in defenders:
            if defender.get_position().equals(position):
                self._last_hit = True
                defender.set_text("X")
                defender.set_color(globals.RED_BOLD)
                return 
        
        # if no hit, create a new shot actor in cast 
        shot = Actor()
        shot.set_position(position)
        shot.set_text("X")
        shot.set_color(globals.WHITE)
        self._cast.add_actor("artillery", shot)
        return 

    # method to set ship color
    def set_color(self, color):
        """This method will accept a color and set the ship to that color

        parameters: color (Color) - a color to paint the ship
        returns: nothing
        """
        self._red, self._green, self._blue, self._alpha = color.to_tuple()

    # method to return ship color
    def get_color(self):
        """This method will return the full color spectrum of the ship

        parameters: none
        returns: color (Color) - the full ship color spectrum
        """
        return Color(self._red, self._green, self._blue, self._alpha)