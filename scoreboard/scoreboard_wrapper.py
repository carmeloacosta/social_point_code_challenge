#!/bin/python3

"""
    Wrapper to give access to the shared Scoreboard.
"""

from constants import DEFAULT_IP, DEFAULT_PORT, CLIENT_MODE, SERVER_MODE


class ScoreboardWrapper():
    """

    """
    def __init__(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        self.ip = ip
        self.port = port

    def start(self, mode):
        """

        :param mode:
        :return:
        """
        if mode == CLIENT_MODE:
            pass

        elif mode == SERVER_MODE:
            pass

    def update(self, client_info):
        """
            Sends updated client score to the shared Scoreboard.

        :param client_info: (dict) A JSON submitted by the client, as specified in the Code Challenge:

                Examples:

                            {"user": 123, "total": 250}
                            {"user": 456, "score": "+10"}
                            {"user": 789, "score": "-20"}

        :return: (dict) The updated client score.
        """
        pass

    def top(self, top_size):
        """
            Asks the shared Scoreboard for the clients that occupy the specified number of top ranking positions
            (i.e., those with the higher score values), according to the absolute ranking.

        :param top_size: (int) Number of higher ranking positions to retrieve.
        :return: (list of dict) The clients that occupies the specified ranking positions.
        """
        pass

    def relative_top(self, ranking_position, scope_size):
        """
            Asks the shared Scoreboard for the relative top (see Scoreboard.relative_top)

        :param ranking_position: (int) Ranking position to retrieve scope around. Must be a positive value, from 1 to N.
        :param scope_size: (int) Scope size (see explanation above). Must be a positive value.
        :return: (list of dict) The clients that occupies the specified ranking positions.
        """
        pass
