#!/bin/python3

"""
    Scoreboard module. Contains all information regarding with a scoreboard that keeps the ranking of all clients
"""

from bintrees import FastAVLTree

import os
os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path

from client import Client


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
        # Allows to access sorted info in O(log(N))
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
        #import ipdb; ipdb.set_trace() #DEBUGGING
        try:
            #
            # Handle first report/old sorting order
            #
            client_id = int(client_info["user"])

            if client_id not in self.clients:
                # First client report
                self.clients[client_id] = Client(client_id)

            else:
                # Remove client prior score, since it is going to be modified
                prior_score = self.clients[client_id].score
                if len(self.sorted_clients[prior_score]) > 1:
                    # There are other clients with that score
                    self.sorted_clients[prior_score].remove(self.clients[client_id])
                else:
                    # The only one with that score
                    del self.sorted_clients[prior_score]

            #
            # Compute/Update new score
            #
            try:
                result = self.clients[client_id].total(client_info["total"])
            except KeyError:
                # Try with relative update
                result = self.clients[client_id].relative(client_info["score"])

            #
            # Update/restore client sorting order
            #
            new_score = self.clients[client_id].score
            if new_score not in self.sorted_clients:
                # First client with that score. Initialize an empty list to hold all users with that same score.
                self.sorted_clients.insert(new_score, [])

            self.sorted_clients[new_score].append(self.clients[client_id])

        except (KeyError, ValueError):
            # Invalid client_info
            result = False

        return result

    def top(self, top_size):
        """
            Returns the clients that occupy the specified number of top ranking positions (i.e., those with the higher
                score values), according to the absolute ranking.

            IMPLEMENTATION NOTE: If more than one clients are tied in a given position the returned list considers them
                as a single ranking position.
                Example: ({"user": 123, "total": 100}, {"user": 456, "total": 200}, {"user": 789, "total": 100})

                    The top-2 (i.e., top_size = 2) is:

                    [1st-{"user": 456, "total": 200},
                     2nd-{"user": 123, "total": 100}
                     2nd-{"user": 789, "total": 100}
                    ]

        :param top_size: (int) Number of higher ranking positions to retrieve.
        :return: (list of Client) The clients that occupies the specified ranking positions.
        """
        result = []
        try:
            top_positions = self.sorted_clients.nlargest(top_size)
            for position in top_positions:
                result.extend(position[1])
        except TypeError:
            pass

        return result

