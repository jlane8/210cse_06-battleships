"""
file: video_service.py
author: authors of rfk
purpose: This class handles the video output of Battleships.
"""
# import module used to create and display on game screen
import pyray

# class declaration
class VideoService:
    """Outputs the game state. The responsibility of the class of objects is to draw the game state 
    on the screen. 

    Attributes:
        _caption - displays the window's name
        _width - the width of the display window
        _height - the height of the display window
        _cell_size - a division used to align text
        _frame_rate - how fast the screen will redraw all elements
        _debug - used when debugging
    """

    # default constructor
    def __init__(self, caption, width, height, cell_size, frame_rate, debug = False):
        """Constructs a new VideoService using the specified debug mode.
        
        Args:
            debug (bool): whether or not to draw in debug mode.

        Returns:
            nothing
        """
        
        # store values internally
        self._caption = caption
        self._width = width
        self._height = height
        self._cell_size = cell_size
        self._frame_rate = frame_rate
        self._debug = debug

    # method to release computer resources and close game window
    def close_window(self):
        """Closes the window and releases all computing resources.
        
        Args: 
            none

        Returns:
            nothing
        """
        pyray.close_window()

    # method to erase space in preparation of drawing next scene
    def clear_buffer(self):
        """Clears the buffer in preparation for the next rendering. This method should be called at
        the beginning of the game's output phase.

        Args: 
            none

        Returns:
            nothing
        """
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        if self._debug == True:
            self._draw_grid()
    
    # method to draw next actor in buffer
    def draw_actor(self, actor):
        """Draws the given actor's text on the screen.

        Args:
            actor (Actor): The actor to draw.

        Returns:
            nothing
        """ 
        text = actor.get_text()
        x = actor.get_position().get_x()
        y = actor.get_position().get_y()
        font_size = actor.get_font_size()
        color = actor.get_color().to_tuple()
        pyray.draw_text(text, x, y, font_size, color)
        
    # method to draw multiple actors in buffer
    def draw_actors(self, actors):
        """Draws the text for the given list of actors on the screen.

        Args:
            actors (list): A list of actors to draw.

        Returns:
            nothing
        """ 
        for actor in actors:
            self.draw_actor(actor)
    
    # method to write what is in the buffer onto the screen
    def flush_buffer(self):
        """Copies the buffer contents to the screen. This method should be called at the end of
        the game's output phase.

        Arg:
            none

        Returns:
            nothing
        """ 
        pyray.end_drawing()

    # method to return the current cell size
    def get_cell_size(self):
        """Gets the video screen's cell size.
        
        Args:
            none
        
        Returns:
            Grid: The video screen's cell size.
        """
        return self._cell_size

    # method to return current screen height
    def get_height(self):
        """Gets the video screen's height.
        
        Args:
            none

        Returns:
            Grid: The video screen's height.
        """
        return self._height

    # method to return current screen width
    def get_width(self):
        """Gets the video screen's width.
        
        Args:
            none

        Returns:
            Grid: The video screen's width.
        """
        return self._width

    # method return True if the user has not closed it 
    def is_window_open(self):
        """Whether or not the window was closed by the user.

        Args:
            none

        Returns:
            bool: True if the window is closing; false if otherwise.
        """
        return not pyray.window_should_close()

    # method to create the game window
    def open_window(self):
        """Opens a new window with the provided title.

        Args:
            title (string): The title of the window.

        Returns:
            nothing
        """
        pyray.init_window(self._width, self._height, self._caption)
        pyray.set_target_fps(self._frame_rate)

    # method to segment the game screen
    def _draw_grid(self):
        """Draws a grid on the screen.
        
        Args:
            none

        Returns:
            nothing
        """
        for y in range(0, self._height, self._cell_size):
            pyray.draw_line(0, y, self._width, y, pyray.GRAY)
        for x in range(0, self._width, self._cell_size):
            pyray.draw_line(x, 0, x, self._height, pyray.GRAY)