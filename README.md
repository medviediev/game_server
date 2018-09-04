# Psycho game server

Game server with api based on Flask micro framework. It works with Flask development server from the box.

The implemented task consists into elaborating an update system for a large number of players distributed on a map.
- The logic of the task executed in proportion of 100% on the server.
- The programming language used for the implementation is Python.
- The DB used for the data storing is MongoDB.

The server itself is as follows:

There is a map that consists in a **config.MAP_WIDTH** x **config.MAP_HEIGHT** rectangle, where a number of 
**config.PLAYERS_NUMBER** players are randomly created and distributed.
Each of the players can trigger up to **config.MAX_PLAYER_TASKS** tasks on the server. 
Each task consist of only a timer which is stored and updated on the server.
Info about each player stored as a document in the MongoDB database **config.DATABASE_NAME** collection
**config.PLAYERS_COLLECTION**.
The timer for each task is between **config.MIN_TASK_DURATION** seconds and **config.MAX_TASK_DURATION** seconds.
If the time of a task expires, the task is considered completed and then it is dismissed (erased from the DB).
Each player has a field of view around him of **config.VISIBLE_AREA_WIDTH** x **config.VISIBLE_AREA_HEIGHT** squares
(meaning that he can see what players around him do on this area) (activate it using api).
Each of the players will start task(s) on the server with a random frequency. In case they have already
reached the maximum number of tasks started, they have to wait until they are finished to start a new one.
At any time player’s field of view can be randomly changes on the map to see different portions of it
(activate it using api). Logs are available in **visible_area.log** file.
When the server boots, the DB is populated with data in an automated way only if it is empty.
By populating with data it is mean that players will be added to the DB, so that we have **config.PLAYERS_NUMBER**
players in the database, with one (1) or more tasks started.
Logs with all events happening on server are available in the MongoDB database **config.DATABASE_NAME** collection
**config.LOG_COLLECTION** and in the **world_events.log** file (who, when and where executed the task).

**REST API** for getting info about one player (with his surrounding context: players who are in his field of view
area, their tasks) and it's log control, all players (with their personal data only) and control 
stop currently running, create new ones) player’s tasks are provided. Check **api_docs.md**.

----

## Getting Started

### Prerequisites

It's recommended to use **MongoDB**, **Python 3.7** with **pipenv** as virtual environment.

Check [python.org](https://www.python.org) to install **Python 3.7**.
Check [mongodb.com](https://docs.mongodb.com/manual/installation/) to install **MongoDB**.

Install pipenv:

```
pip install pipenv
```

### Installing

It's better to use **pipenv** or other virtual environment for using the server.

To create **pipenv** virtual environment with all dependencies go to the app path and use:

```
python -m pipenv shell
python -m pipenv install
```

To specify **python** version to use with virtual environment use:

```
pipenv shell --python 3.x
```

Or check **Pipfile** to install dependencies manually without **pipenv** using **pip**:

```
pip install package_name
```

### Running

Check **config.py** file before you start.

It's better to use pipenv or other virtual environment for starting the server.

To activate **pipenv** go to the app path and use:

```
python -m pipenv shell
```

To start server on **Windows** with existed **pipenv** go to the app path and use:

```
>set FLASK_APP=app.py
>python -m flask run
 * Running on http://127.0.0.1:5000/
```

To start server on **Unix** with existed **pipenv** go to the app path and use:

```
$ export FLASK_APP=app.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/
```

To ensure everything works fine go to the index page:

```
http://127.0.0.1:5000/
```

Config page is available at:

```
http://127.0.0.1:5000/server_config
```

## Tests

Game server API tests are provided with **test_api.py**.

To activate **pipenv** go to the app path and use:

```
python -m pipenv shell
```

To run tests go to the app path and use:

```
python -m unittest test_api.py -v
 * Running on http://127.0.0.1:5000/
```

## Authors

* **Oleksandr Medviediev** - [will.be.psychedelic@gmail.com](https://mailto:will.be.psychedelic@gmail.com)
