"""
file: director.py
author: author of rfk and Jerry Lane
purpose: This class directs the game action.
"""
# import the global values, the Point class, and the Actor class
import globals
from game.shared.point import Point
from game.casting.actor import Actor

# class declaration
class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    # default constructor
    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._is_game_over = False
        self._enter_key_up = False
        self._enter_key_down = False
        self._hit_scored = False
        self._enemy_hit_scored = False
        self._enemy_destroyed = False
        self._defender_destroyed = False
        self._ships_are_revealed = False

    # method holding game loop
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        # open game window
        self._video_service.open_window()

        # align cursor with enemy grid
        cursor = cast.get_first_actor("cursors")
        x = int((globals.MAX_X / 2) / globals.CELL_SIZE) 
        y = int(((globals.MAX_Y - globals.CELL_SIZE) / 4) / globals.CELL_SIZE) 
        cursor.set_position(Point(x, y).scale(globals.CELL_SIZE))

        # main game loop
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    # method getting inputs
    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the cursor.
        
        Args:
            cast (Cast): The cast of actors.
        """
        # get cursor from cast, get velocity from keys, move cursor
        cursor = cast.get_first_actor("cursors")
        velocity = self._keyboard_service.get_direction()
        cursor.set_velocity(velocity)   
        
        # if game over, set enemy ships to show, return
        if self._is_game_over:
            if self._ships_are_revealed == False:
                self._ships_are_revealed = True
                ships = cast.get_actors("enemy_ships")
                for i in range(len(ships)):
                    ships[i].set_color(globals.RED_BOLD)
            return

        # check if enter key is down
        if self._keyboard_service.get_enter_key_state():
            self._enter_key_down = True

        # check if enter key is up
        if self._keyboard_service.is_enter_key_up():
            self._enter_key_up = True

    # method updating game play
    def _do_updates(self, cast):
        """Updates the cursor's position and resolves any collisions with ships.
        
        Args:
            cast (Cast): The cast of actors.

        Returns: 
            nothing
        """
        # set hit scored, enemy hit, and damaged bools to false
        self._hit_scored = False
        self._enemy_hit_scored = False

        # get banners from cast for messages
        banner = cast.get_first_actor("banners")

        # get cursor from cast
        cursor = cast.get_first_actor("cursors")

        # get fleets from cast
        ships = cast.get_actors("enemy_ships")
        defenses = cast.get_actors("defense_ships")

        # get screen width and height from video service, then move cursor
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        cursor.move_next(max_x, max_y)
        
        # loop through enemy ships
        for ship in ships:
            
            # check to see if the ship position equals the cursor position and the Enter key has been pressed.
            if self._enter_key_down and self._enter_key_up and ship.get_position().equals(cursor.get_position()):
                
                # show Enter key used
                self._enter_key_down = False
                self._enter_key_up = False 
                
                # if so, set the color to visible, change the text to an X for destroyed, and let the ship's message go on the banner
                ship.set_color(globals.RED_BOLD)
                ship.set_text("X")
                banner.set_text("Enemy ship hit!")
                
                # set hit scored flag                    
                self._hit_scored = True

                # enemy returns fire
                self._return_fire(cast)

        # if the enter key been down and back up and player missed, do the following
        if self._enter_key_down and self._enter_key_up and not self._hit_scored:

            # show Enter key as used
            self._enter_key_down = False
            self._enter_key_up = False  
            
            # create new shot actor and put in cast
            shot = Actor()
            shot.set_position(cursor.get_position())
            shot.set_text("X")
            shot.set_color(globals.WHITE)
            cast.add_actor("artillery", shot)
            banner.set_text("")

            # enemy returns fire
            self._return_fire(cast)

        # check to see if enemy is destroyed, set flag appropriately
        self._enemy_destroyed = True
        for ship in ships:
            if ship.get_text() != "X":
                self._enemy_destroyed = False
        
        # check to see if defenders are destroyed, set flag appropriately
        self._defender_destroyed = True
        for defender in defenses:
            if defender.get_text() != "X":
                self._defender_destroyed = False

        # if either the enemy or defender fleet is destroyed, end game
        if self._enemy_destroyed or self._defender_destroyed:
            if self._enemy_destroyed:
                win_message = "You Win! Game over."
            else:
                win_message = "The enemy prevailed. You lose."
            banner.set_text(win_message)
            self._is_game_over = True
    
    # enemy returns fire method
    def _return_fire(self, cast):
        """Enemy returns fire up to 75% of working ships

        Args:
            cast (Cast): assembly of all actors

        Returns:
            nothing        
        """
        # get banners
        # get needed cast members
        ships = cast.get_actors("enemy_ships")
        banner = cast.get_first_actor("banners")
        banner_2 = cast.get_second_actor("banners")

        # find out how many enemy ships are left
        return_fire = self._count_ships(cast, "enemy_ships")
        
        # if 2 or more, number of return fire is 75% of working ships
        if return_fire >= 2:
            return_fire = int(return_fire * .75)

        # see how many defense ships are left
        pre_volley = self._count_ships(cast, "defense_ships")
        
        # conduct enemy return fire
        for i in range(return_fire):
            self._enemy_hit_scored = ships[i].target()
        
        # see how many defense ships are left and determine loss
        post_volley = self._count_ships(cast, "defense_ships")
        loss = pre_volley - post_volley
        ships_left = use_word = ""
        
        # keep words used correct to numbers
        if post_volley == 1:
            ship_word = "ship"
        else:
            ship_word = "ships"
        if loss == 1:
            use_word = "ship"
        else:
            use_word = "ships"

        # see how many enemy ships are working, and give report to player  
        banner.set_text(f"Enemy ships left: {return_fire}")
        banner_2.set_text(f"Damage Report: {loss} {use_word} damaged, {post_volley} {ship_word} left.")

    # method to count number of casualties
    def _count_ships(self, cast, group):
        """Gets the number of undamaged ships and returns it.

        Args:
            cast (Cast): cast of all actors
            group (String): selection of cast members to get

        Returns:
            count (int): integer of how many defense ships remain
        """
        # get functioning defense forces from cast, count them out, return count 
        forces = cast.get_actors(group)
        count = len(forces)
        for force in forces:
            if force.get_text() == "X":
                count -= 1
        return count
        
    # method to perform all outputs
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.

        Returns:
            nothing
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()