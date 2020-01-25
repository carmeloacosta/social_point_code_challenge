import os
import unittest
from json import dumps, loads
from unittest.mock import MagicMock
from multiprocessing import Process

os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path

from app import start_scoreboard_client, start_scoreboard_server
from constants import DEFAULT_IP, DEFAULT_PORT, CLIENT_MODE, SERVER_MODE


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #
        # Setup a real server
        #
        DEBUG_MODE = True
        cls.server_app = Process(target=start_scoreboard_server, args=(DEFAULT_PORT, DEFAULT_IP, not DEBUG_MODE))
        cls.server_app.start()

        #
        # Setup a client in DEBUG_MODE
        #
        cls.client_app = start_scoreboard_client(DEFAULT_PORT, DEFAULT_IP, DEBUG_MODE)

    @classmethod
    def tearDownClass(cls):
        cls.server_app.terminate()

    def setUp(self):
        self.client = self.client_app.test_client()
        self.client.delete('/reset')
        self.maxDiff = None

    def test_score_ok(self):

        client_msg = {"user": 123, "total": 250}

        # Test main
        response = self.client.put('/score', data=dumps(client_msg), content_type='application/json')

        # Check results
        body = response.data.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(body), client_msg)

    def test_top_ok(self):

        top_size = 100
        expected_top = [{"user": 123, "total": 250}, {"user": 456, "total": 200}, {"user": 789, "total": 100}]

        #
        # Prepopulate according to expected
        #
        for user_msg in expected_top:
            response = self.client.put('/score', data=dumps(user_msg), content_type='application/json')

            self.assertEqual(response.status_code, 200)

        # Test main
        response = self.client.get('/top/{}'.format(top_size))

        # Check results
        body = response.data.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(body), expected_top)

    def test_relative_top_ok(self):

        ranking_position = 2
        scope_size = 1
        expected_top = [{"user": 123, "total": 250}, {"user": 456, "total": 200}, {"user": 789, "total": 100}]

        #
        # Prepopulate according to expected
        #
        for user_msg in expected_top:
            response = self.client.put('/score', data=dumps(user_msg), content_type='application/json')

            self.assertEqual(response.status_code, 200)

        # Test main
        response = self.client.get('/top/{}/{}'.format(ranking_position, scope_size))

        # Check results
        body = response.data.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(body), expected_top)
