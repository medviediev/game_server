"""
Module with classes describing api request behaviour.
"""


from flask import request
from flask_restful import Resource
import bson
import app
from map_vision import MapVision
from task_assignment import TaskAssigner


def verify_player_id():

    """
    Verify player's id. Id must be bson's ObjectId and presents in players MongoDB collection.
    :return: player dict from MongoDB collection if player exists or None
    :rtype: dict
    """

    # Get player's id from URL
    player_id = request.args.get('player_id', type=str)

    # Convert str player's id to bson's ObjectId
    try:
        player_id_obj = bson.ObjectId(player_id)
    except bson.errors.InvalidId:
        return None

    # Find player in in players MongoDB collection by id
    main_player = app.players_collection.find_one({'_id': player_id_obj})

    return main_player


def get_area_center_coordinates(player):

    """
    Get x and y coordinates from URL or assign player's position coordinates as the center of the area.
    :param player: player's dict
    :type player: dict
    :return: x, y as the center of the area coordinates
    :rtype: tuple of two ints
    """

    # Get x and y coordinates from URL
    x = request.args.get('x', default=-1, type=int)
    y = request.args.get('y', default=-1, type=int)

    # Use player's position coordinated if x and y are not specified in the request or exceed the map
    if x < 0 or x > app.app.config['MAP_WIDTH'] or y < 0 or y > app.app.config['MAP_HEIGHT']:
        x = player['x']
        y = player['y']

    return x, y


class GetPlayer(Resource, MapVision):

    """
    Class for getting one player info with it's visible area info.
    """

    def get(self):

        """
        Api get request handling.
        :return: dict object as response
        :rtype: dict
        """

        # Verify player's id
        main_player = verify_player_id()

        # Return error if player does not exist
        if main_player is None:
            return {'error': 'wrong player_id'}, 400

        # Get x and y coordinates
        x, y = get_area_center_coordinates(main_player)

        # Calculate visible area coordinates
        area = self.calculate_visible_area_coordinates(x, y, app.app.config['VISIBLE_AREA_WIDTH'],
                                                       app.app.config['VISIBLE_AREA_HEIGHT'])

        # Get MongoDB collection cursor for all players within visible area
        visible_players = self.get_area_players(area, app.players_collection)

        # Prepare all players within visible area info
        visible_players_list = []

        for player in visible_players:

            player['_id'] = str(player['_id'])
            visible_players_list.append(player)

        # Prepare current player info
        main_player['_id'] = str(main_player['_id'])

        if main_player in visible_players_list:
            visible_players_list.remove(main_player)

        result = {'current_player': main_player, 'center_x': x, 'center_y': y, 'visible_players': visible_players_list}

        return result, 200


class GetPlayers(Resource):

    """
    Class for getting players personal info. Number of players to show can be specified with limit request attribute.
    By default all players personal info will be showed.
    """

    @staticmethod
    def get():

        """
        Api get request handling.
        :return: dict object as response
        :rtype: dict
        """

        # Get number of players limit from URL
        limit = request.args.get('limit', default=app.app.config['PLAYERS_NUMBER'], type=int)
        # Get MongoDB collection cursor for players
        players = app.players_collection.find({}, limit=limit)

        # Prepare players info
        players_list = []

        for player in players:

            player['_id'] = str(player['_id'])
            players_list.append(player)

        result = {'players': players_list}

        return result, 200


class TasksControl(Resource):

    """
    Class for player's tasks control.
    """

    @staticmethod
    def get():

        """
        Api get request handling.
        :return: dict object as response
        :rtype: dict
        """

        # Verify player's id
        main_player = verify_player_id()

        # Return error if player does not exist
        if main_player is None:
            return {'error': 'wrong player_id'}, 400

        # Get control trigger from URL
        control = request.args.get('control', default=1, type=int)

        # Stop all player's tasks if control is 0 or start new tasks if else
        if control and main_player['_id'] in TaskAssigner._players_to_stop:
            TaskAssigner._players_to_stop.remove(main_player['_id'])
        else:
            TaskAssigner._players_to_stop.append(main_player['_id'])

        result = {'player_id': str(main_player['_id']), 'control': control}

        return result, 200


class AreaPlayersLogControl(Resource, MapVision):

    """
    Class for starting visible area logging.
    """

    def get(self):

        """
        Api get request handling.
        :return: dict object as response
        :rtype: dict
        """

        # Get control trigger from URL
        control = request.args.get('control', default=0, type=int)

        # Stop visible area logging if control is 0
        if not control:
            MapVision.stop_area_players_logging()
            return {'area_players_log': control}, 200

        # Verify player's id
        main_player = verify_player_id()

        # Return error if player does not exist
        if main_player is None:
            return {'error': 'wrong player_id'}, 400

        # Get x and y coordinates
        x, y = get_area_center_coordinates(main_player)

        # Calculate visible area coordinates
        area = self.calculate_visible_area_coordinates(x, y, app.app.config['VISIBLE_AREA_WIDTH'],
                                                       app.app.config['VISIBLE_AREA_HEIGHT'])
        # Start visible area logging
        self.start_visible_area_logging(area, app.players_collection)

        result = {'player_id': str(main_player['_id']), 'center_x': x, 'center_y': y, 'area_players_log': control}

        return result, 200
