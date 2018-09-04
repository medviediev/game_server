# Flask app settings
DEBUG = True

# MongoDB settings
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DATABASE_NAME = 'game'
PLAYERS_COLLECTION = 'players'
LOG_COLLECTION = 'log'

# World initialization settings
MAP_WIDTH = 512
MAP_HEIGHT = 512
PLAYERS_NUMBER = 20000

# Task assignment setting
ASSIGN_ON_BOOT = 1
MAX_PLAYER_TASKS = 4
MIN_TASK_DURATION = 10
MAX_TASK_DURATION = 600
DEFAULT_TASK_DELAY = 1

# Visible area settings
VISIBLE_AREA_WIDTH = 32
VISIBLE_AREA_HEIGHT = 32

# Logging settings
DEFAULT_LOGGING_DELAY = 1
