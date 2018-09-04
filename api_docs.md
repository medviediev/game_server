# Psycho game server API description

**Get one player info**

    Returns json data about a single player with his surrounding context: players who are in his field of view area,
    their tasks. The field can be changed with specific coordinates.

* **URL**

    /api/get_player

* **Method:**

    `GET`
  
* **URL Params**

    **Required:**
 
    `player_id=[string(bson.ObjectId)]`
   
    **Optional**
    
    Specific visible area coordinates. Player's current position by default.
   
    `x=[integer]`
   
    `y=[integer]`

* **Success Response:**

    * **Code:** 200 <br />
      **Content:** `{"current_player": {"_id": "5b8d00f01fb4b888d84d8f13", "x": 0, "y": 1, "Task 1": 1535982634.7317052},
      "center_x": 0, "center_y": 15, "visible_players": [{"_id": "5b8d00f01fb4b888d84d8f36", "x": 1, "y": 7,
      "Task 1": 1535982483.702951}]}`
 
* **Error Response:**

    * **Code:** 400 <br />
      **Content:** `{'error': 'wrong player_id'}`

* **Sample Call:**

    ```
    http://127.0.0.1:5000/api/get_player?player_id=5b8d00f01fb4b888d84d8f13&x=10&y=20
    ```

----

**Get batch of players info**

    Returns json data about batch of players personal info. The amount of returned players info can be changed.

* **URL**

    /api/get_players

* **Method:**

    `GET`
  
* **URL Params**
   
    **Optional**
    
    The amount of returned players info. All players by default.
   
    `limit=[integer]`

* **Success Response:**

    * **Code:** 200 <br />
      **Content:** `{"players": [{"_id": "5b8d00f01fb4b888d84d8f13", "x": 0, "y": 15, "Task 1": 1535982808.7297094},
      {"_id": "5b8d00f01fb4b888d84d8f14", "x": 0, "y": 57, "Task 1": 1535982904.5918064}]}`

* **Sample Call:**

    ```
    http://127.0.0.1:5000/api/get_players?limit=100
    ```
    
----

**Player tasks control**

    Request to stop currently running or create new player’s tasks. 
    Returns json data about a single player with his tasks status: 1 for active, 0 for inactive.

* **URL**

    /api/tasks_control

* **Method:**

    `GET`
  
* **URL Params**

    **Required:**
 
    `player_id=[string(bson.ObjectId)]`
   
    **Optional**
    
    Control trigger - 0 to stop all current tasks, 1 (by default) - to start new tasks.
   
    `control=[integer]`

* **Success Response:**

    * **Code:** 200 <br />
      **Content:** `{"player_id": "5b8d00f01fb4b888d84d8f13", "control": 0}`
 
* **Error Response:**

    * **Code:** 400 <br />
      **Content:** `{'error': 'wrong player_id'}`

* **Sample Call:**

    ```
    http://127.0.0.1:5000/api/tasks_control?player_id=5b8d00f01fb4b888d84d8f13&control=0
    ```

----

**Visible area log control**

    Request to start or to stop visible area logging. Logs are available in visible_area.log. 
    Returns json data about a visible area logging status: 1 for active, 0 for inactive.

* **URL**

    /api/area_log

* **Method:**

    `GET`
  
* **URL Params**

    Without params stops logging
   
    **Optional**
    
    Control trigger - 0 (by default) to stop visible area logging, 1 - to start visible area logging.
   
    `control=[integer]`
    
    Current player's id
    
    `player_id=[string(bson.ObjectId)]`
    
    Specific visible area coordinates. Player's current position by default.
   
    `x=[integer]`
   
    `y=[integer]`

* **Success Response:**

    * **Code:** 200 <br />
      **Content:** `{"player_id": "5b8d00f01fb4b888d84d8f13", "center_x": 0, "center_y": 15, "area_players_log": 1}`
 
* **Error Response:**

    * **Code:** 400 <br />
      **Content:** `{'error': 'wrong player_id'}`

* **Sample Call:**

    ```
    http://127.0.0.1:5000/api/area_log?player_id=5b8d00f01fb4b888d84d8f13&control=1
    ```
