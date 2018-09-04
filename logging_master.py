"""
Module for logs handling.
"""


import logging
import time


def init_logger(logger_name):

    """
    Logger initialization.
    :param logger_name: logger name
    :type logger_name: str
    :return: logger
    """

    # Create new logger
    logger = logging.getLogger(logger_name)
    # Set logging level
    logger.setLevel(logging.INFO)
    # Create new file handler
    file_handler = logging.FileHandler(f'{logger_name}.log', mode='w')
    # Add handler to logger
    logger.addHandler(file_handler)

    return logger


def make_player_log_note(player):

    """
    Make log note from player's dict.
    :param player: player's dict
    :type player: dict
    :return: log note
    :rtype: str
    """

    tasks = []

    for key, value in player.items():

        if 'Task' in key:

            time_left = time.strftime('%Mm:%Ss',  time.gmtime(value - time.time()))
            tasks.append(f'{key}, timeLeft {time_left};')

    tasks = ' '.join(tasks)

    log_note = f'Player[{player["x"]},{player["y"]}] {tasks}'

    return log_note


def make_task_log_note(player, task_id, task_status, duration=''):

    """
    Make task log note.
    :param player: player's dict
    :type player: dict
    :param task_id: task id
    :type task_id: str
    :param task_status: task status - 1 for start and 0 for finish
    :type task_status: int
    :param duration: task duration in seconds
    :type duration: int
    :return: log note
    :rtype: str
    """

    if task_status:
        status = 'started'
    else:
        status = 'finished'

    log_time = time.strftime('%H:%M:%S',  time.gmtime(time.time()))
    log_note = f'{log_time} Player[{player["x"]},{player["y"]}] {task_id} {status}'

    if duration:
        log_note += f' will finished in {duration} s'

    return log_note
