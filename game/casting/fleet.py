import globals
import random
from game.casting.cast import Cast
from game.casting.ship import Ship
from game.shared.point import Point

class Fleet(Cast):
    

    def __init__(self, cast):
        
        super().__init__()
        self._fleet = {}
        self._build = []
        self._enemies = []
        self._defenders = []
        self._message = ""
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
        for i in range(7, 1, -1):
            self._create_ship(i, location, color)
            self.add_ship(group, self._build.copy())  
    
    # create ship
    def _create_ship(self, length, location, color):

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
                ship = Ship(self._cast)

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
                ship.set_color(self._color)
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
                    fleet = self.get_ships("enemy_ships")
                else:
                    fleet = self.get_ships("defense_ships")
                
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
    def add_ship(self, group, ship):
        
        if not group in self._fleet.keys():
            self._fleet[group] = []
            
        if not ship in self._fleet[group]:
            self._fleet[group].append(ship)
    
    # method to return the ship list
    def get_ships(self, group):
        results = []
        if group in self._fleet.keys():
            results = self._fleet[group].copy()
        return results

    # method to get all ships
    def get_all_ships(self):
        results = []
        for group in self._fleet:
            results.extend(self._fleet[group])
        return results

    # method to return a ship
    def get_ship(self, group, id):
        return self._fleet[group][id]

    # method to return the ship list
    def get_build(self):
        return self._build






    
    
    def get_all_actors(self):
        """Gets all of the actors in the cast.
        
        Returns:
            List: All of the actors in the cast.
        """
        