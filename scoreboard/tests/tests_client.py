import os
import unittest

os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path

from client import Client


class TestClient(unittest.TestCase):

    def test_client_creation_ok(self):

        client_id = 987

        # Test main
        client = Client(client_id)

        # Check results
        self.assertEqual(client.id, client_id)
        self.assertEqual(client.score, 0)

    def test_client_total_ok(self):

        client_id = 986
        total_list = [10, 100, 150, 75, 225]

        # Test main
        client = Client(client_id)

        for new_total in total_list:
            client.total(new_total)

            # Check results
            self.assertEqual(client.id, client_id)
            self.assertEqual(client.score, new_total)

    def test_client_relative_ok(self):

        client_id = 985
        # (<relative_score>, <total_score>)
        relative_list = [("+10", 10), ("-100", -90), ("+150", 60), ("-75", -15), ("+225", 210)]

        # Test main
        client = Client(client_id)

        for new_relative, new_total in relative_list:

            success = client.relative(new_relative)

            # Check results
            self.assertEqual(success, True)
            self.assertEqual(client.id, client_id)
            self.assertEqual(client.score, new_total)

    def test_client_relative_wrong(self):

        client_id = 984
        relative_list = ["10", "-", "+", "+1xaY50", "*75", ]

        # Test main
        client = Client(client_id)

        for new_relative in relative_list:

            success = client.relative(new_relative)

            # Check results
            self.assertEqual(success, False)

    def test_client_total_sorting_ok(self):

        client_id_list = [1, 2, 3, 4, 5, 6]
        client_score_list = [100, 200, 150, 350, 225, 155]
        expected_sorted_id_list = [4, 5, 2, 6, 3, 1]
        self.assertEqual(len(client_id_list), len(client_score_list))
        self.assertEqual(len(client_score_list), len(expected_sorted_id_list))

        client_list = []
        for ptr, client_id in enumerate(client_id_list):
            new_client = Client(client_id)
            new_client.total(client_score_list[ptr])
            client_list.append(new_client)

        # Test main
        sorted_client_list = sorted(client_list, key=lambda obj: obj.score, reverse=True)

        # Check results
        self.assertEqual(len(client_id_list), len(sorted_client_list))

        for ptr in range(len(sorted_client_list)):
            self.assertEqual(sorted_client_list[ptr].id, expected_sorted_id_list[ptr])
