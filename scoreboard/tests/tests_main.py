import os
import unittest

os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path
from main import main


class TestMain(unittest.TestCase):

    def test_main_ok(self):
        self.assertEqual(main(), True)
