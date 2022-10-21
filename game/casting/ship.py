"""
File: ship.py
Author: Jerry Lane
Purpose: The Ship class holds the infomation on an Actor that is
also a ship.
"""

# import global values
import globals
import random

# since an Artifact inherits from Actor, import Actor
from game.casting.actor import Actor
from game.shared.color import Color
from game.shared.point import Point

# class declaration
class Ship(Actor):
    """
    Parameters: none
    Return: nothing
    The Ship class holds the description of the ship actor in its 
    member 'message.'
    """

    # constructor method for Artifact
    # TODO - change to include location attribute parameter to show where the ships should be drawn on screen
    # and inclue a bool variable to track whether the Enter key is up or down to prevent multiple actions from
    # the Enter key being down.
    def __init__(self, cast):
        """
        Parameters: none
        Return: nothing
        The constructor method merely sets the default message of an Artifact
        instantiation to nothing ("").
        """
        # inherit the constructor elements of the Actor class
        super().__init__()

        # initialize attributes
        self._message = ""
        self._cast = cast
        self._history = [Point(900, 900), Point(900, 900), \
            Point(900, 900), Point(900, 900), Point(900, 900)]

    # set_message method to set description of the artifact instantiation
    def set_message(self, message):
        """
        Parameters: message - descriptive text of artiface
        Return: nothing
        The set_message method does just that; it sets the descriptive message of
        an artifact instantiation.
        """
        # internal _message variable set to the parameter message
        self._message = message

    # get_message method will return the description contained in _message
    def get_message(self):
        """
        Parameter: none
        Return: _message - the descriptive text set by the set_message method
        The get_message method returns the private _message variable descriptive 
        text.
        """
        # return the _message variable's descriptive text
        return self._message
                        
    # method to return the ship list
    def get_ship(self):
        return self._ship


    # TODO - write ai targeting code somewhere - doesn't have to be here
    def target(self):
        """
        parameters: none
        return: bool - True if hit, False if not
        
        structure of self._history is:

                         _history[1]
        _history[0]  _history[2]  _history[3]
                         _history[5]

        Point(900, 900) indicates this location has not been tried
        Point(800, 800) indicates this location missed
        All points inside the screen indicate a hit
        """

        # set some defaults
        miss = Point(800, 800)
        blank = Point(900, 900)

        # set area boundaries
        x_left = globals.CELL_SIZE
        x_right = globals.MAX_X
        y_bottom = globals.MAX_Y - globals.CELL_SIZE
        y_top = int(y_bottom / 2) + globals.CELL_SIZE

        # # check hit history, if there was a previous hit, flag previous_hit
        # for i in range(len(self._history)):
        #     if not self._history[i].equals(Point(900, 900)):
        #         previous_hit = True
        #     else:
        #         previous_hit = False

        # # check to see if last attempt hit, if not, guess a new point
        # if not previous_hit:
            
        # choose random x, y point within defender area
        x = int((random.randint(x_left, x_right)) / globals.CELL_SIZE)
        y = int(random.randint(y_top, y_bottom - globals.CELL_SIZE) / globals.CELL_SIZE)
        position = Point(x, y).scale(globals.CELL_SIZE)
        
        # check to see if it hit, if so, update _history
        if self._check_for_hit(position):
            # self._history[2] = position
            return True
        
        else:
            return False

        # # there was a previous hit, so we follow up
        # else:

        #     # get last primary hit coordinates
        #     current_x = self._history[2].get_x()
        #     current_y = self._history[2].get_y()

        #     # code logic to determine this attack location
        #     # if blank, attempt right
        #     if self._history[3].equals(blank):
                
        #         # check for boundary
        #         if current_x < x_right - globals.CELL_SIZE:
        #             position = Point(current_x + globals.CELL_SIZE, current_y)
        #             if self._check_for_hit(position):
        #                 self._history[3] = position
        #                 return True
        #         else:
        #             self._history[3] = miss
        #             return False 
            
        #     # if right of hit isn't blank, attempt left
        #     elif self._history[0].equals(blank):

        #         # check for boundary
        #         if current_x > globals.CELL_SIZE:
        #             position = Point(current_x - globals.CELL_SIZE, current_y)
        #             if self._check_for_hit(position):
        #                 self._history[0] = position
        #                 return True
        #         else:
        #             self._history[0] = miss
        #             return False 

        #     # if horizontal failed, try down 
        #     elif self._history[4].equals(blank):

        #         # check for boundary
        #         if current_y < y_bottom - globals.CELL_SIZE:
        #             position = Point(current_x, current_y + globals.CELL_SIZE)
        #             if self._check_for_hit(position):
        #                 self._history[4] = position
        #                 return True
        #         else:
        #             self._history[4] = miss
        #             return False 

        #     # if vertical failed on bottom, try up 
        #     elif self._history[1].equals(blank):

        #         # check for boundary
        #         if current_y > y_top + globals.CELL_SIZE:
        #             position = Point(current_x, current_y - globals.CELL_SIZE)
        #             if self._check_for_hit(position):
        #                 self._history[4] = position
        #                 return True
        #         else:
        #             self._history[4] = miss
        #             return False 

        #     # if left two are hits, try left again
        #     elif not self._history[0].equals(blank) and not self._history[0].equals(miss):

        #         # check for boundary
        #         if self._history[0].get_x() > globals.CELL_SIZE:
        #             position = Point(self._history[0].get_x() - globals.CELL_SIZE, current_y)
        #             if self._check_for_hit(position):
        #                 self._history[1] = blank
        #                 self._history[4] = blank
        #                 self._history[3] = self._history[2]                       
        #                 self._history[2] = self._history[0]
        #                 self._history[0] = position            
        #                 return True
        #         else:
        #             self._zero_hit_history()
        #             return False                 
            
        #     # if right two are hits, try right again
        #     elif not self._history[3].equals(blank) and not self._history[3].equals(miss):

        #         # check for boundary
        #         if self._history[3].get_x() <= x_right - globals.CELL_SIZE:
        #             position = Point(self._history[3].get_x() + globals.CELL_SIZE, current_y)
        #             if self._check_for_hit(position):
        #                 self._history[1] = blank
        #                 self._history[0] = self._history[2] 
        #                 self._history[2] = self._history[3]
        #                 self._history[4] = blank
        #                 self._history[3] = position                                  
        #                 return True
        #         else:
        #             self._zero_hit_history()
        #             return False

        #     # if top two are hits, try up again
        #     elif not self._history[1].equals(blank) and not self._history[1].equals(miss):

        #         # check for boundary
        #         if self._history[1].get_y() >  y_top + globals.CELL_SIZE:
        #             position = Point(current_x, self._history[1].get_y() - globals.CELL_SIZE)
        #             if self._check_for_hit(position):
        #                 self._history[0] = blank
        #                 self._history[3] = blank
        #                 self._history[4] = self._history[2]                       
        #                 self._history[2] = self._history[1]
        #                 self._history[1] = position            
        #                 return True
        #         else:
        #             self._zero_hit_history()
        #             return False

        #     # if bottom two are hits, try down again
        #     elif not self._history[4].equals(blank) and not self._history[4].equals(miss):

        #         # check for boundary
        #         if self._history[4].get_y() <=  y_bottom - globals.CELL_SIZE:
        #             position = Point(current_x, self._history[1].get_y() + globals.CELL_SIZE)
        #             if self._check_for_hit(position):
        #                 self._history[0] = blank
        #                 self._history[3] = blank
        #                 self._history[1] = self._history[2]                       
        #                 self._history[2] = self._history[4]
        #                 self._history[4] = position            
        #                 return True
        #         else:
        #             self._zero_hit_history()
        #             return False

        #     # if nothing else has worked, reset and try from scratch
        #     else:
        #         self._zero_hit_history() 
        #         return False              

    def _zero_hit_history(self):
        self._history = [Point(900, 900), Point(900, 900), \
            Point(900, 900), Point(900, 900), Point(900, 900)] 
    
    def _check_for_hit(self, position):
        
        # get defense fleet information
        defenders = self._cast.get_actors("defense_ships")

        # loop position against positions of all defenders
        for defender in defenders:
            if defender.get_position().equals(position):
                self._last_hit = True
                defender.set_text("X")
                defender.set_color(globals.RED_BOLD)
                return True
        
        # if no hit, create new shot actor 
        shot = Actor()
        shot.set_position(position)
        shot.set_text("X")
        shot.set_color(globals.WHITE)
        self._cast.add_actor("artillery", shot)
        return False