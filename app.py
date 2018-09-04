"""
Game server with api based on Flask micro framework.
"""


from flask import Flask, render_template
from flask_restful import Api
from pymongo import MongoClient
from world_initialization import WorldCreator
from task_assignment import TaskAssigner
import api_classes


# Create main app with api
app = Flask(__name__)
app.config.from_object('config')
api = Api(app)

# Connect to MongoDB
mongo_client = MongoClient(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
database = mongo_client[app.config['DATABASE_NAME']]
players_collection = database[app.config['PLAYERS_COLLECTION']]
log_collection = database[app.config['LOG_COLLECTION']]

# Check if database exists and there are some players
if app.config['DATABASE_NAME'] not in mongo_client.list_database_names() or not players_collection.count_documents({}):

    creator = WorldCreator(app.config['MAP_WIDTH'], app.config['MAP_HEIGHT'], app.config['PLAYERS_NUMBER'])
    new_world = creator.generate_new_world()
    creator.save_world(players_collection, new_world)

# Get all players from the collection
players = players_collection.find()

# Assign tasks for each player
if app.config['ASSIGN_ON_BOOT']:

    task_assigner = TaskAssigner(players_collection, log_collection)
    task_assigner.start_task_assignment(players)

# Setup api
api.add_resource(api_classes.GetPlayer, '/api/get_player')
api.add_resource(api_classes.GetPlayers, '/api/get_players')
api.add_resource(api_classes.TasksControl, '/api/tasks_control')
api.add_resource(api_classes.AreaPlayersLogControl, '/api/area_log')


@app.route('/')
def index():

    """
    Main page view.
    :return: rendered main page
    """

    # Get players number
    current_players = players_collection.count_documents({})

    return render_template('index.html', current_players=current_players)


@app.route('/server_config')
def server_config():

    """
    Server config page view.
    :return: rendered config page page
    """

    # Get all the configs
    with open('config.py', 'r') as file:
        current_config = file.read().splitlines()

    return render_template('server_config.html', current_config=current_config)


if __name__ == '__main__':

    app.run()
