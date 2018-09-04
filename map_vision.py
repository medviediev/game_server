"""
Module for working with visible area on the map.
"""


import time
import threading
import app
import logging_master


class MapVision:

    """
    Class for working with visible area on the map.
    """

    # Logging trigger attribute
    _logging_thread = False

    def visible_area_logging(self, area, db_collection):

        """
        Visible area logging.
        :param area: area coordinates
        :type area: tuple
        :param db_collection: MongoDB players collection
        :return: None
        """

        # Initiate new logger
        logger = logging_master.init_logger('visible_area')

        # Continue logging while logging trigger attribute is True
        while MapVision._logging_thread:

            # Get MongoDB collection cursor for all players within visible area
            area_players = self.get_area_players(area, db_collection)

            # Add log note for each player within visible area
            for player in area_players:

                log_note = logging_master.make_player_log_note(player)
                logger.info(log_note)

            # Delay between log notes
            time.sleep(app.app.config['DEFAULT_LOGGING_DELAY'])

    def start_visible_area_logging(self, area, db_collection):

        """
        Start visible area logging in new Thread.
        :param area: area coordinates
        :type area: tuple
        :param db_collection: MongoDB players collection
        :return: None
        """

        # Set logging trigger attribute to True
        MapVision._logging_thread = True

        # Start visible area logging in new Thread
        thread = threading.Thread(target=self.visible_area_logging, args=(area, db_collection))
        thread.start()

    @staticmethod
    def stop_area_players_logging():

        """
        Stop visible area logging.
        :return: None
        """

        # Set logging trigger attribute to False
        MapVision._logging_thread = False

    @staticmethod
    def calculate_visible_area_coordinates(center_x, center_y, width, height):

        """
        Calculate visible area coordinates that are described with area's edge points.
        :param center_x: x coordinate of area center
        :type center_x: int
        :param center_y: y coordinate of area center
        :type center_y: int
        :param width: area width
        :type width: int
        :param height: area height
        :type height: int
        :return: coordinates of area's edge points
        :rtype: tuple
        """

        # Calculate shift from the center
        half_width = int(width / 2)
        half_height = int(height / 2)

        # Calculate area's edge points
        left_x = center_x - half_width
        right_x = center_x + half_width
        lower_y = center_y - half_height
        upper_y = center_y + half_height

        # Make area's edge points tuple
        area_coordinates = (left_x, right_x, lower_y, upper_y)

        return area_coordinates

    @staticmethod
    def get_area_players(area, db_collection):

        """
        Get MongoDB collection cursor for all players within visible area.
        :param area: area coordinates
        :type area: tuple
        :param db_collection: MongoDB collection
        :return: cursor for all players within visible area
        """

        area_players = db_collection.find({'x': {'$gte': area[0], '$lte': area[1]},
                                           'y': {'$gte': area[2], '$lte': area[3]}})

        return area_players
