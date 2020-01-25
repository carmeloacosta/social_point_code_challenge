import os
import unittest
from json import dumps, loads
from unittest.mock import MagicMock

os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path

from api import get_api
from scoreboard_wrapper import ScoreboardWrapper


class TestApi(unittest.TestCase):

    def setUp(self):
        self.scoreboard_wrapper = ScoreboardWrapper()
        self.app = get_api(self.scoreboard_wrapper)
        self.client = self.app.test_client()
        self.maxDiff = None

    def test_score_ok(self):

        client_msg = {"user": 123, "total": 250}
        self.scoreboard_wrapper.update = MagicMock(return_value=client_msg)

        # Test main
        response = self.client.put('/score', data=dumps(client_msg), content_type='application/json')

        # Check results
        body = response.data.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(body), client_msg)

    def test_top_ok(self):

        top_size = 100
        expected_top = [{"user": 123, "total": 250}, {"user": 456, "total": 200}, {"user": 789, "total": 100}]
        self.scoreboard_wrapper.top = MagicMock(return_value=expected_top)

        # Test main
        response = self.client.get('/top/{}'.format(top_size))

        # Check results
        body = response.data.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(body), expected_top)
        self.scoreboard_wrapper.top.assert_called_with(top_size)

    def test_relative_top_ok(self):

        ranking_position = 2
        scope_size = 1
        expected_top = [{"user": 123, "total": 250}, {"user": 456, "total": 200}, {"user": 789, "total": 100}]
        self.scoreboard_wrapper.relative_top = MagicMock(return_value=expected_top)

        # Test main
        response = self.client.get('/top/{}/{}'.format(ranking_position, scope_size))

        # Check results
        body = response.data.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(body), expected_top)
        self.scoreboard_wrapper.relative_top.assert_called_with(ranking_position, scope_size)
