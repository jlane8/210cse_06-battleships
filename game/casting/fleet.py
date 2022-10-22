"""
file: fleet.py
author: Jerry Lane
purpose: This class builds and maintains the fleets of ships for 
the enemy and the defender.
"""
# import modules
import globals
import random
from game.casting.cast import Cast
from game.casting.ship import Ship
from game.shared.point import Point

# class declaration
class Fleet(Cast):
    """The Fleet class represents all the ships, on both sides.
    Attributes:
        _fleet{} - holds the fleet (enemy or defender) 
        _built[] - holds the ship being built
        _group - whether enemy or defender
        _length - length of ships
        _text - holds ship text
        _location - determines where the ships is built
        _cast - holds all the actors in the game
        _creating_ship - flag on whether or not the ship is being built
        _color - fleet base color
    """

    # default constructor
    def __init__(self, cast):
        """This constructs both of the fleets.

        parameters: cast (Cast) - holds the entirety of the actors in the game
        returns: nothing
        """
        # load parent constructor
        super().__init__()

        # prepare to build ships, then build fleets
        self._fleet = {}
        self._build = []
        self._group = ""
        self._length = 0
        self._text = ""
        self._location = 0
        self._cast = cast
        self._creating_ship = True
        self._color = globals.WHITE
        self._create_fleet("enemy_ships", "upper", globals.RED)
        self._create_fleet("defense_ships", "lower", globals.GREEN)
    
    # create fleet
    def _create_fleet(self, group, location, color):
        """This method creates a fleet of either enemy ships or defender ships
        parameters: group (String) - key to store fleet under
                    location (int) - indicates whether to build the fleet in enemy or defender space
                    color (Color) - paint the fleet this color
        returns: nothing
        """
        # build six groups of ships of different amounts, store in cast
        for i in range(7, 1, -1):
            self._create_actor(i, location, color)
            self.add_actor(group, self._build.copy())  
    
    # create ship group
    def _create_actor(self, length, location, color):
        """This method builds each group of ships that go into a fleet.
        parameters: length (int) - number of ships in group
                    locations (int) - enemy or defender fleet
                    color (Color) - color of ships
            return: nothing
        """
        # set location, group, length, build, and color
        if location == "upper":
            self._location = 0
            self._group = "enemy_ships"
        else:
            self._location = ((globals.MAX_Y - globals.CELL_SIZE) / 2) + globals.CELL_SIZE
            self._group = "defense_ships"
        self._length = length
        self._build = []
        self._color = color
        
        # set absolute bottom of screen that can be used for ship construction
        max_y = globals.MAX_Y - globals.CELL_SIZE

        # turn on loop
        self._creating_ship = True
        
        # select position of ship construction, if there is a conflict, do it again
        while self._creating_ship:
        
            # assume one pass is all that is needed
            self._creating_ship = False

            # set limits for ship builds, top for enemy, bottom for defender
            x = int(random.randint(globals.CELL_SIZE, globals.MAX_X - (self._length * globals.CELL_SIZE)) / globals.CELL_SIZE)
            if self._location == 0:
                y = int(random.randint(globals.CELL_SIZE, int(max_y / 2) - globals.CELL_SIZE - (self._length * globals.CELL_SIZE)) / globals.CELL_SIZE)
            else:
                y = int(random.randint(int(max_y / 2) + globals.CELL_SIZE, max_y - globals.CELL_SIZE - (self._length * globals.CELL_SIZE)) / globals.CELL_SIZE)
            position = Point(x, y)

            # orient the ship north/south (0) or east/west (1)
            orient = random.randint(0, 1)

            # build the ship
            for n in range (self._length):
                
                # scale position according to cell size
                self._position = position.scale(globals.CELL_SIZE)
                
                # declare new ship
                ship = Ship(self._cast, color)

                # build the fore, aft, and midship
                ship.set_text("=")
                if n == 0 and orient == 1:
                    ship.set_text("<")
                elif n == self._length - 1 and orient == 1:
                    ship.set_text(">")
                elif n == 0 and orient == 0:
                    ship.set_text("^")
                elif n == self._length - 1 and orient == 0:
                    ship.set_text("=")
                
                # set the ship font size, color, and position 
                ship.set_font_size(globals.FONT_SIZE)
                ship.set_position(self._position)

                # add section of ship to the whole
                self._build.append(ship)
                
                # set up for next section build
                if orient == 0:
                    y += 1
                else:
                    x += 1
                position = Point(x, y)

            # if this isn't the first ship created
            if self._length != 7:
                
                # get appropriate cast members for enemy or defense fleet
                if self._group == "enemy_ships":
                    fleet = self.get_actors("enemy_ships")
                else:
                    fleet = self.get_actors("defense_ships")
                
                # check to see if any ships overlap, if so run this loop again
                for section in self._build:
                    for vessel in fleet:
                        for segment in vessel:
                            if segment.get_position().equals(section.get_position()):
                                self._creating_ship = True
                
                # if two ships overlapped, erase current ship list, build anew
                if self._creating_ship:
                    self._build = []

    # add ship to fleet
    def add_actor(self, group, ship):
        """This method adds a ship formation to the group fleet.

        parameters: group (String) - denotes enemy_ships or defense_ships
                    ship (Ship) - newly constructed ship
           returns: nothing
        """
        # if group is not in the fleet keys, add it
        if not group in self._fleet.keys():
            self._fleet[group] = []
        
        # if ship is not already in the fleet group, add it
        if not ship in self._fleet[group]:
            self._fleet[group].append(ship)
    
    # method to return the ship list
    def get_actors(self, group):
        """This method gets all the ships in the group fleet.
        parameters: group (String) - denotes which fleet to return
        returns: results[] (List) - fleet information by group
        """
        # clear list
        results = []

        # if the group is in the fleet keys, put it in the list and return
        if group in self._fleet.keys():
            results = self._fleet[group].copy()
        return results

    # method to get all ships
    def get_all_actors(self):
        """This method returns all the ships in the fleets.
        
        parameters: none
        returns: results[] (List) - contains all the ships in the fleets.
        """

        # clear list
        results = []

        # put all ships in the fleet in the results list and return
        for group in self._fleet:
            results.extend(self._fleet[group])
        return results

    # method to return a ship
    def get_actor(self, group, id):
        """This method will return a specific ship based on group and id.

        parameters: group (String) - holds the name of the fleet.
                    id (int) - holds the element number of the ship
        returns: ship (Ship) - as noted in specified group and id
        """
        return self._fleet[group][id]

    # method to return the ship build list
    def get_build(self):
        """This method returns the ship list that was just built.
        
        parameters: none
        returns: _build (List) - contains the ship formation just built.
        """
        return self._build        