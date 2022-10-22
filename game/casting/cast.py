"""
file: cast.py
author: authors of rfk and Jerry Lane
purpose: This class will contain all of the actors in the game.
"""

# class declaration
class Cast:
    """A collection of actors.

    The responsibility of a cast is to keep track of a collection of actors. It has methods for 
    adding, removing and getting them by a group name.

    Attributes:
        _actors (dict): A dictionary of actors { key: group_name, value: a list of actors }
    """

    # default constructor
    def __init__(self):
        """Constructs a new Actor.
        
        parameters: none
        returns: nothing
        """
        self._actors = {}
    
    # method to add an actor to the cast
    def add_actor(self, group, actor):
        """Adds an actor to the given group.
        
        Args:
            group (string): The name of the group.
            actor (Actor): The actor to add.
        Returns:
            nothing
        """
        # if actor not in actors keys, add it
        if not group in self._actors.keys():
            self._actors[group] = []
        
        # if actor is not in the group, add it
        if not actor in self._actors[group]:
            self._actors[group].append(actor)

    def get_actors(self, group):
        """Gets the actors in the given group.
        
        Args:
            group (string): The name of the group.

        Returns:
            results (List): The actors in the group.
        """
        # clear list
        results = []
        
        # if group is in the actors keys, put into list and return
        if group in self._actors.keys():
            results = self._actors[group].copy()
        return results
    
    def get_all_actors(self):
        """Gets all of the actors in the cast.
        
        Parameters: 
            none

        Returns:
            result (List): All of the actors in the cast.
        """
        # clear results lis
        results = []

        # put all actors in the results list
        for group in self._actors:
            results.extend(self._actors[group])
        return results

    def get_first_actor(self, group):
        """Gets the first actor in the given group.
        
        Args:
            group (string): The name of the group.
            
        Returns:
            List: The first actor in the group.
        """
        # clear result
        result = None

        # put first element of group into the result variable and return
        if group in self._actors.keys():
            result = self._actors[group][0]
        return result

    def get_second_actor(self, group):
        """Gets the first actor in the given group.
        
        Args:
            group (string): The name of the group.
            
        Returns:
            List: The first actor in the group.
        """
        # clear result
        result = None

        # put second element of group into result variable and return
        if group in self._actors.keys():
            result = self._actors[group][1]
        return result

    def remove_actor(self, group, actor):
        """Removes an actor from the given group.
        
        Args:
            group (string): The name of the group.
            actor (Actor): The actor to remove.
        Returns:
            nothing
        """
        #if actor is in the group, remove it
        if group in self._actors:
            self._actors[group].remove(actor)