import os
import unittest
from multiprocessing import Process
os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path


from scoreboard_wrapper import ScoreboardWrapper
from constants import DEFAULT_IP, DEFAULT_PORT, CLIENT_MODE, SERVER_MODE


def start_server(port):
    server = ScoreboardWrapper()
    server.start(SERVER_MODE)


class TestScoreboardWrapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup server
        cls.server = Process(target=start_server, args=(DEFAULT_PORT, ))
        cls.server.start()

        cls.client = ScoreboardWrapper()
        cls.client.start(CLIENT_MODE)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()

    def setUp(self):
        self.client.reset()

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
        wrapper = ScoreboardWrapper(port, ip)

        # Check results
        self.assertEqual(wrapper.ip, ip)
        self.assertEqual(wrapper.port, port)

    def test_update_ok(self):

        #client = ScoreboardWrapper()
        #self.client.start(CLIENT_MODE)
        client_info = {"user": 123, "total": 250}

        # Test main
        result = self.client.update(client_info)

        # Check results
        self.assertEqual(result, client_info)

    def test_single_client_total_ok(self):

        client_id = 123
        total_list = [{"user": client_id, "total": 250},
                      {"user": client_id, "total": 100},
                      {"user": client_id, "total": 150},
                      {"user": client_id, "total": 75},
                      {"user": client_id, "total": 225}
                      ]

        #client = ScoreboardWrapper()
        #self.client.start(CLIENT_MODE)

        # Test main
        for new_total in total_list:
            result = self.client.update(new_total)

            # Check results
            self.assertEqual(result, new_total)

    def test_single_client_relative_ok(self):

        client_id = 124
        relative_list = [{"user": client_id, "score": "+10"},
                         {"user": client_id, "score": "-100"},
                         {"user": client_id, "score": "+150"},
                         {"user": client_id, "score": "-75"},
                         {"user": client_id, "score": "+225"}
                         ]

        expected_total = [10, -90, 60, -15, 210]

        self.assertEqual(len(relative_list), len(expected_total))

        #client = ScoreboardWrapper()
        #self.client.start(CLIENT_MODE)

        # Test main
        for ptr, new_relative in enumerate(relative_list):
            result = self.client.update(new_relative)

            # Check results
            self.assertEqual(result["user"], client_id)
            self.assertEqual(result["total"], expected_total[ptr])

    def test_single_client_relative_wrong(self):

        client_id = 125
        relative_list = [{"user": client_id, "score": "10"},
                         {"user": client_id, "score": "-"},
                         {"user": client_id, "score": "+"},
                         {"user": client_id, "score": "+1xaY50"},
                         {"user": client_id, "score": "*75"}
                         ]

        #client = ScoreboardWrapper()
        #self.client.start(CLIENT_MODE)

        # Test main
        for new_relative in relative_list:
            result = self.client.update(new_relative)

            self.assertEqual(result, {"error": "Invalid client info"})

    def test_multiple_client_total_sorting_ok(self):

        client_id_list = [1, 2, 3, 4, 5, 6]
        client_score_list = [100, 200, 150, 350, 225, 155]
        expected_sorted_id_list = [4, 5, 2, 6, 3, 1]
        self.assertEqual(len(client_id_list), len(client_score_list))
        self.assertEqual(len(client_score_list), len(expected_sorted_id_list))

        #client = ScoreboardWrapper()
        #self.client.start(CLIENT_MODE)

        for ptr in range(len(client_id_list)):
            self.client.update({"user": client_id_list[ptr], "total": client_score_list[ptr]})

        # Test main
        sorted_client_list = self.client.top(len(client_id_list))

        # Check results
        self.assertEqual(len(client_id_list), len(sorted_client_list))

        for ptr in range(len(sorted_client_list)):
            self.assertEqual(sorted_client_list[ptr]["user"], expected_sorted_id_list[ptr])

    def test_multiple_client_top_ok(self):

        client_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        client_score_list = [100, 200, 150, 350, 225, 155, 60, 415, 190, 25]
        expected_sorted_id_list = [8, 4, 5, 2, 9, 6, 3, 1, 7, 10]
        self.assertEqual(len(client_id_list), len(client_score_list))
        self.assertEqual(len(client_score_list), len(expected_sorted_id_list))

        #client = ScoreboardWrapper()
        #self.client.start(CLIENT_MODE)

        for ptr in range(len(client_id_list)):
            self.client.update({"user": client_id_list[ptr], "total": client_score_list[ptr]})

        # Test main
        top_size = 3
        sorted_client_list = self.client.top(top_size)

        # Check results
        self.assertEqual(len(sorted_client_list), top_size)

        for ptr in range(top_size):
            self.assertEqual(sorted_client_list[ptr]["user"], expected_sorted_id_list[ptr])

    def test_multiple_client_relative_top_ok_and_wrong(self):

        client_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        client_score_list = [100, 200, 150, 350, 225, 155, 60, 415, 190, 25]
        expected_sorted_id_list = [8, 4, 5, 2, 9, 6, 3, 1, 7, 10]
        self.assertEqual(len(client_id_list), len(client_score_list))
        self.assertEqual(len(client_score_list), len(expected_sorted_id_list))

        #
        # (<ranking_position>, <scope_size>, <description>)
        #
        #  where:
        #
        #       <ranking_position>: (int) The ranking_position
        #       <scope_size>: (int) The scope_size
        #       <expected_result_size>: (int) Size of the expected result
        #       <description>: (str) Human friendly description of the scenario
        scenario_list = [
            (-3, 2, 0, "Range does not exists"),
            (5, -2, 0, "Range does not exists"),
            (5, 2, 5, "Full range exists"),
            (11, 2, 2, "Range truncated on the right (not enough low scores)"),
            (1, 2, 3, "Only truncated on the left (enough low scores)"),
            (5, 8, 10, "Range truncated both on the left and on the right (not enough neither low nor high scores)")
        ]

        for scenario in scenario_list:

            ranking_position = scenario[0]
            scope_size = scenario[1]
            expected_result_size = scenario[2]

            # These are the ranking positions to be obtained
            position_ptr_list = []
            for value in range(scope_size, 0, -1):
                ptr = ranking_position-1-value
                if (ptr >= 0) and (ptr < len(expected_sorted_id_list)):
                    position_ptr_list.append(ptr)

            for value in range(scope_size+1):
                ptr = ranking_position-1+value
                if (ptr >= 0) and (ptr < len(expected_sorted_id_list)):
                    position_ptr_list.append(ptr)

            self.assertEqual(len(position_ptr_list), expected_result_size)

            #client = ScoreboardWrapper()
            #self.client.start(CLIENT_MODE)

            for ptr in range(len(client_id_list)):
                self.client.update({"user": client_id_list[ptr], "total": client_score_list[ptr]})

            # Test main
            sorted_client_list = self.client.relative_top(ranking_position, scope_size)

            # Check results
            self.assertEqual(len(sorted_client_list), expected_result_size)

            for idx, ptr in enumerate(position_ptr_list):
                self.assertEqual(sorted_client_list[idx]["user"], expected_sorted_id_list[ptr])
