import os
import unittest

os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path


from scoreboard_wrapper import ScoreboardWrapper
from constants import DEFAULT_IP, DEFAULT_PORT


class TestScoreboardWrapper(unittest.TestCase):

    def test_empty_creation_ok(self):

        # Test main
        wrapper = ScoreboardWrapper()

        # Check results
        self.assertEqual(wrapper.ip, DEFAULT_IP)
        self.assertEqual(wrapper.port, DEFAULT_PORT)

    def test_creation_ok(self):

        ip = "192.168.1.1"
        port = 9000
        self.assertNotEqual(ip, DEFAULT_IP)
        self.assertNotEqual(port, DEFAULT_PORT)

        # Test main
        wrapper = ScoreboardWrapper(ip, port)

        # Check results
        self.assertEqual(wrapper.ip, ip)
        self.assertEqual(wrapper.port, port)


