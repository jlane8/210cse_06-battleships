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

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the cursor.
        
        Args:
            cast (Cast): The cast of actors.
        """
        # get cursor from cast, get velocity from keys, move cursor
        cursor = cast.get_first_actor("cursors")
        velocity = self._keyboard_service.get_direction()
        cursor.set_velocity(velocity)   
        
        # if game over, return
        if self._is_game_over:
            return

        # check if enter key is down
        if self._keyboard_service.get_enter_key_state():
            self._enter_key_down = True

        # check if enter key is up
        if self._keyboard_service.is_enter_key_up():
            self._enter_key_up = True

    def _do_updates(self, cast):
        """Updates the cursor's position and resolves any collisions with ships.
        
        Args:
            cast (Cast): The cast of actors.
        """
        # set hit scored bool to false
        self._hit_scored = False
        self._enemy_hit_scored = False
        self._damaged = False

        # get banners from cast for messages
        banner = cast.get_first_actor("banners")
        banner_2 = cast.get_second_actor("banners")

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
            
            # check to see if the ship position equals the cursor position and the Enter key is pressed.
            if self._enter_key_down and self._enter_key_up and ship.get_position().equals(cursor.get_position()):

                # TODO UNCOMMENT WHEN DONE TROUBLESHOOTING 
                
                # show Enter key used
                self._enter_key_down = False
                self._enter_key_up = False 
                

                # if so, set the color to visible, change the text to an X for destroyed, and let the ship's message go on the banner
                ship.set_color(globals.RED_BOLD)
                ship.set_text("X")
                banner.set_text("Enemy ship hit!")
                
                # enemy fires back
                return_fire = self._enemy_left(cast)
                pre_volley = self._count_damage(cast)
                for i in range(return_fire):
                    self._enemy_hit_scored = ships[i].target()
                post_volley = self._count_damage(cast)
                if pre_volley > post_volley:
                    banner_2.set_text("The enemy damaged our ships.")
                else:
                    banner_2.set_text("")

                # set hit scored flag                    
                self._hit_scored = True

        if self._enter_key_down and self._enter_key_up and not self._hit_scored:

            # TODO - UNCOMMENT WHEN DONE TROUBLESHOOTING 

            # show Enter key as used
            self._enter_key_down = False
            self._enter_key_up = False  
            
            # create new shot actor 
            shot = Actor()
            shot.set_position(cursor.get_position())
            shot.set_text("X")
            shot.set_color(globals.WHITE)
            cast.add_actor("artillery", shot)
            banner.set_text("")
            
            # enemy fires back
            return_fire = self._enemy_left(cast)
            pre_volley = self._count_damage(cast)
            for i in range(return_fire):
                self._enemy_hit_scored = ships[i].target()
            post_volley = self._count_damage(cast)
            if pre_volley > post_volley:
                banner_2.set_text("The enemy damaged our ships.")
            else:
                banner_2.set_text("")

        # check to see if enemy is destroyed
        self._enemy_destroyed = True
        for ship in ships:
            if ship.get_text() != "X":
                self._enemy_destroyed = False
        
        # check to see if defenders are destroyed
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






        # cursor_position = cursor.get_position()
        # ship = ships[0].get_position()
        # banner.set_text(f"Cursor: {cursor_position.get_x()}, {cursor_position.get_y()} | Ship: {ship.get_x()}, {ship.get_y()}")
        
    # method to determine how many enemy ships can return fire
    def _enemy_left(self, cast):
        count = 0
        enemies = cast.get_actors("enemy_ships")
        for enemy in enemies:
            if enemy.get_text() != "X":
                count += 1
        return count
    
    # method to count number of casualties
    def _count_damage(self, cast):
        count = 0
        defenses = cast.get_actors("defense_ships")
        for defense in defenses:
            if defense.get_text() == "X":
                count += 1
        return count
        
    # method to perform all outputs
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()