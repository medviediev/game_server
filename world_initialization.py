"""
Module for new world initialization. Includes map creation and random players distribution.
"""


import numpy as np


class WorldCreator:

    """
    Class for new world creation.
    """

    def __init__(self, map_width, map_height, players_number):

        """
        Instance initialization.
        :param map_width: map width
        :type map_width: int
        :param map_height: map height
        :type map_height: int
        :param players_number: number of players
        :type players_number: int
        """

        # Raise value error if there are too many players
        if players_number > map_height * map_width:
            raise ValueError('Map size is too small for such amount of players!')

        self.map_width = map_width
        self.map_height = map_height
        self.players_number = players_number

    @staticmethod
    def generate_blank_map(size):

        """
        Generate blank map as an array of False elements.
        :param size: map size
        :type size: int
        :return: blank map as an array of False elements
        :rtype: np.ndarray
        """

        blank_map = np.zeros(size, dtype=bool)

        return blank_map

    @staticmethod
    def generate_players(number):

        """
        Generate players as an array of True elements.
        :param number: number of players
        :type number: int
        :return: players as an array of True elements
        :rtype: np.ndarray
        """

        players = np.ones(number, dtype=bool)

        return players

    def distribute_players_per_map(self, target_map, players):

        """
        Randomly distribute players within the map.
        :param target_map: blank map as an array of False elements
        :param players: players as an array of True elements
        :return: map with randomly distributed players as 2D array
        :rtype: np.ndarray
        """

        # Concatenate map array and players array
        filled_map = np.concatenate((target_map, players))
        # Shuffle elements
        np.random.shuffle(filled_map)

        # Reshape 1D array to 2D
        world = np.reshape(filled_map, (self.map_width, self.map_height))

        return world

    def generate_new_world(self):

        """
        Generating new world. Consists of a map with randomly distributed players.
        :return: map with randomly distributed players as 2D array
        :rtype: np.ndarray
        """

        # Calculate blank map size
        blank_map_size = self.map_width * self.map_height - self.players_number
        # Generate blank map as an array of False elements
        blank_map = self.generate_blank_map(blank_map_size)
        # Generate players as an array of True elements
        players = self.generate_players(self.players_number)
        # Randomly distribute players within the map
        world = self.distribute_players_per_map(blank_map, players)

        return world

    @staticmethod
    def make_players_identities(world):

        """
        Make players identities basing on their position on the map (2D array indices).
        :param world: map with randomly distributed players as 2D array
        :type world: np.ndarray
        :return: generator for player identities
        """

        # Generator to convert 2D array indices into player's coordinates
        for coordinates in zip(*np.where(world)):

            yield {'x': int(coordinates[0]), 'y': int(coordinates[1])}

    def save_world(self, db_collection, world):

        """
        Save players identities to MongoDB collection
        :param db_collection: MongoDB collection
        :param world: map with randomly distributed players as 2D array
        :type world: np.ndarray
        :return: None
        """

        # Use generator to generate player identity and insert it to MongoDB collection
        for player in self.make_players_identities(world):

            db_collection.insert_one(player)
