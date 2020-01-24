#!/bin/python3

"""
    Scoreboard module. Contains all information regarding with a scoreboard that keeps the ranking of all clients
"""

from bintrees import FastAVLTree

from .client import Client


class ScoreBoard():
    """
        Keeps Scoreboard info
    """
    def __init__(self):
        # Clients that have reported score
        #   <key> :<value> -> <client_id> : <client>
        #
        #   where:
        #
        #           <client_id> (int) : Id that uniquelly specifies the client.
        #           <client> (Client) : Information of the client (including score)
        #
        self.clients = {}

        # AVL tree in which each node is a list of Client instances (i.e., all the clients with the same score)
        self.sorted_clients = FastAVLTree()

    def update(self, client_info):
        """
            Modifies the client total score.

        :param client_info: (dict) A JSON submitted by the client, as specified in the Code Challenge:

                Examples:

                            {"user": 123, "total": 250}
                            {"user": 456, "score": "+10"}
                            {"user": 789, "score": "-20"}
        :return: (bool) True if successfully updated; False otherwise.
        """
        try:

            client_id = int(client_info["user"])
            prior_score = self.clients[client_id].score

            if client_id not in self.clients:
                # First client report
                self.clients[client_id] = Client(client_id)

            else:
                # Remove client prior score, since it is going to be modified
                self.sorted_clients[prior_score].remove(self.clients[client_id])

            # Compute new score
            try:
                result = self.clients[client_id].total(client_info["total"])
            except KeyError:
                # Try with relative update
                result = self.clients[client_id].relative(client_info["score"])

        except (KeyError, ValueError):
            # Invalid client_info
            result = False

        return result
