"""
Module for asynchronous players tasks assignment based on asyncio.
"""


import time
from random import randint
import asyncio
import threading
from concurrent.futures import ALL_COMPLETED
import app
import logging_master


class TaskAssigner:

    """
    Class to assign and control asynchronous players tasks.
    """

    # List for storing players that should be stopped
    _players_to_stop = []

    def __init__(self, players_collection, log_collection):

        """
        Instance initialization.
        :param players_collection: MongoDB players collection
        :param log_collection: MongoDB log collection
        """

        self.players_collection = players_collection
        self.log_collection = log_collection
        self.main_loop = asyncio.new_event_loop()
        self.logger = logging_master.init_logger('world_events')

    def insert_log_note(self, player, task_id, task_status):

        """
        Insert log note into MongoDB log collection.
        :param player: player's dict
        :type player: dict
        :param task_id: task id
        :type task_id: str
        :param task_status: task status - 1 for start, 0 for end
        :type task_status: int
        :return: None
        """

        # Make log note
        log_note = {'player_id': player['_id'],
                    'x': player['x'],
                    'y': player['y'],
                    'task_id': task_id,
                    'task_status': task_status,
                    'time': time.time()}

        # Insert log note into MongoDB log collection
        self.log_collection.insert_one(log_note)

    async def assign_task(self, player, task_id):

        """
        Async function to assign and control player's task.
        :param player: player's dict
        :type player: dict
        :param task_id: task id
        :type task_id: str
        """

        # Generate random task's duration time
        duration = randint(app.app.config['MIN_TASK_DURATION'], app.app.config['MAX_TASK_DURATION'])
        # Calculate time till the end of the task (Unix timestamp)
        end_time = time.time() + duration
        # Make player's id filter to perform search in MongoDB collection
        player_filter = {'_id': player['_id']}

        # Update player's MongoDB document with assigned task
        self.players_collection.update_one(player_filter, {'$set': {task_id: end_time}})
        # Insert log note into MongoDB log collection
        self.insert_log_note(player, task_id, task_status=1)
        # Logger logging
        self.logger.info(logging_master.make_task_log_note(player, task_id, task_status=1, duration=duration))

        # Loop to release coroutine every config.DEFAULT_TASK_DELAY seconds till the end of the task or task cancel
        for _ in range(int(duration / app.app.config['DEFAULT_TASK_DELAY'])):

            await asyncio.sleep(app.app.config['DEFAULT_TASK_DELAY'])

            # Cancel assigned task
            if player['_id'] in TaskAssigner._players_to_stop:
                break

        # Update player's MongoDB document with finished task (delete task)
        self.players_collection.update_one(player_filter, {'$unset': {task_id: end_time}})
        # Insert log note into MongoDB log collection
        self.insert_log_note(player, task_id, task_status=0)
        # Logger logging
        self.logger.info(logging_master.make_task_log_note(player, task_id, task_status=0))

    async def assign_player_tasks(self, player):

        """
        Async recursive function to assign and control player's tasks as coroutines.
        :param player: player's dict
        :type player: dict
        :return: async function itself
        """

        # Generate futures of future for each task of randomly generated tasks
        futures = [self.assign_task(player, f'Task {i}') for i in
                   range(1, randint(2, app.app.config['MAX_PLAYER_TASKS'] + 1))]

        # Wait until all tasks will be finished or canceled
        await asyncio.wait(futures, return_when=ALL_COMPLETED)

        # Loop to release coroutine every config.DEFAULT_TASK_DELAY seconds while player's tasks are canceled
        while player['_id'] in TaskAssigner._players_to_stop:
            await asyncio.sleep(app.app.config['DEFAULT_TASK_DELAY'])

        return await self.assign_player_tasks(player)

    async def assign_players_tasks(self, players):

        """
        Async recursive function to assign tasks as coroutines for all the players.
        :param players: MongoDB collection cursor for players
        """

        # Generate futures of future for each player
        futures = [self.assign_player_tasks(player) for player in players]

        await asyncio.wait(futures)

    def run_async_loop(self, players):

        """
        Function to run asyncio loop.
        :param players: MongoDB collection cursor for players
        :return: None
        """

        # Set asyncio event loop
        asyncio.set_event_loop(self.main_loop)
        # Run asyncio event loop
        self.main_loop.run_until_complete(self.assign_players_tasks(players))

    def start_task_assignment(self, players):

        """
        Function to run asyncio loop as separate thread.
        :param players: MongoDB collection cursor for players
        :return: None
        """

        # Create new thread to run asyncio loop
        main_thread = threading.Thread(target=self.run_async_loop, args=(players,))
        # Run separate thread
        main_thread.start()
