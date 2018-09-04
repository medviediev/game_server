"""
Module for testing flask application api basing on unittest.
"""


import unittest
import config


# Set minimal server config
config.MAP_WIDTH = 10
config.MAP_HEIGHT = 10
config.PLAYERS_NUMBER = 3
config.DATABASE_NAME = 'test'
config.ASSIGN_ON_BOOT = 0


import app


class TestFlaskApi(unittest.TestCase):

    """
    Test case for testing flask application api.
    """

    @classmethod
    def setUpClass(cls):

        """
        Setup flask application before class tests.
        """

        # Set app to the testing mode
        app.app.config['Testing'] = True
        cls.app = app.app.test_client()
        # Get any player_id for testing
        player = app.players_collection.find_one()
        cls.player_id = str(player['_id'])

    @classmethod
    def tearDownClass(cls):

        """
        Clean everything after class tests.
        """

        # Drop test database
        app.mongo_client.drop_database(app.app.config['DATABASE_NAME'])
        # Stop area logging
        cls.app.get(f'/api/area_log')

    def test_index_page(self):

        """
        Test index page availability to ensure app is working properly.
        """

        response = self.app.get('/')
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_player_api(self):

        """
        Test Get one player info api.
        """

        response = self.app.get(f'/api/get_player?player_id={self.player_id}&x=0&y=0')
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_players_api(self):

        """
        Test Get batch of players info api.
        """

        response = self.app.get(f'/api/get_players?limit=1')
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_tasks_control_0_api(self):

        """
        Test Player tasks control api with control mode 0.
        """

        response = self.app.get(f'/api/tasks_control?player_id={self.player_id}&control=0')
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_tasks_control_1_api(self):

        """
        Test Player tasks control api with control mode 1.
        """

        response = self.app.get(f'/api/tasks_control?player_id={self.player_id}&control=1')
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_visible_area_log_1_control(self):

        """
        Test Visible area log control api with control mode 1.
        """

        response = self.app.get(f'/api/area_log?player_id={self.player_id}&control=1&x=0&y=0')
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_visible_area_log_0_control(self):

        """
        Test Visible area log control api with control mode 0.
        """

        response = self.app.get(f'/api/area_log')
        status_code = response.status_code

        self.assertEqual(status_code, 200)


if __name__ == '__main__':

    unittest.main()
    # Drop test database after all the tests
