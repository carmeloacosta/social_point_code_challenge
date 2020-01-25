#!/bin/python3

"""
    Wrapper to give access to the shared Scoreboard.
"""

from json import dumps, loads
from pizco import Proxy, Server

from scoreboard import Scoreboard
from constants import DEFAULT_IP, DEFAULT_PORT, CLIENT_MODE, SERVER_MODE


class ScoreboardWrapper():
    """
        Wraps the Scoreboard into two types of remotely accessible components:

            * Server: wraps a real in-memory instance of the Scoreboard and exposes it via a ZMQ socket.
            * Client: connects to a server, redirects attribute request to it, and collect the response.

        Using this kind of wrapper we can easily implement a multiprocess scoreboardwrapper in which multiple clients,
        each one in a different process, listen to a the HTTP RESTful API that the clients will use to access the
        scoreboard. Besides the multiple clients (as many as allowed by the underlying hardware) there will be a single
        server instance, that receives clients communications and keeps the unique and shared Scoreboard instance.

        This is the typical type of situation in which we have to make a commitment in terms of latency. The scalability
        of the final architecture is hindered by the need of keeping the Scoreboard Data Consistency (SDC). The more
        scalable the architecture the harder to keep the SDC. The proposed architecture is the straighforward initial
        approach, that gets rid of the SDC problem by having a single and centralized server that manages the shared
        scoreboard data. Obviously, this makes the server the critical piece of the architecture in terms of latency,
        since all requests must be attended by the same process.

        If the language allows simultaneous execution of multiple threads (Python does not due to the GIL, or Global
        Interpreter Lock), the next straightforward step towards increasing the scalability would be to make the server
        thread-safe and allow multiple read threads plus a single write thread, to simultaneously run on the same
        server. This is implemented using mutual exclusion (mutex) tools (e.g. semaphores) to protect the critical
        section (i.e., the shared data). Read operations, such as Top100, Top200, Top500, and At100/3, can be done
        simultaneously (one per thread). There will be as many simultaneous threads as allowed by the underlying
        hardware. However, whenever a user reported a new score, regardless of it was either absolute or relative, it
        must be assured that no other thread is within the critical section (unless we follow a policy that does not
        need to report 100% accurate scores on each read).

        The next step towards increasing the scalability of our architecture, that is to reduce the latency, would need
        some kind of partition of the single server to allow accessing it in less time. That kind of vertical
        scalability solution would require adding some kind of scheduling mechanism to properly orchestrate all the
        server partitions to keep SDC yielding better performance, in terms of lower latencies.

        In order not to end up with a overdesign situation, the steps towards the scalability of our architecture should
        be guided by a performance analysis, measuring the latency of one step before taking the decision to go for the
        next one. Take into account that the more steps taken the more complexity in our final design, and therefore
        the less maintainable.

    """

    def __init__(self, port=DEFAULT_PORT, ip=DEFAULT_IP):
        self.ip = ip
        self.port = port
        self.mode = None
        self.instance = None  # Server or Proxy, according to mode
        self.scoreboard = None  # The in-memory scoreboard (only in the server)

    def is_valid_info(self, client_info):
        """
            True if the format of the specified client info is as expected.

        :param client_info: (dict) The client info to be checked. The Valid format is:

                    {"user": <client_id>, ("total": <total_score>|"score": <relative_score>)}

                where:
                        <client_id> : (int) Id of the client.
                        <total_score>: (int) Absolute score of the client.
                        <relative_score>: (int) Relative score of the client.

                Examples:

                            {"user": 123, "total": 250}
                            {"user": 456, "score": "+10"}
                            {"user": 789, "score": "-20"}
        :return:
        """
        result = False

        try:
            if isinstance(client_info, dict) and len(client_info) == 2 and isinstance(client_info["user"], int):
                try:
                    if isinstance(client_info["total"], int):
                        result = True

                except KeyError:
                    # There is no "total" (absolute). Try with "score" (relative)

                    if isinstance(client_info["score"], str) and (client_info["score"][0] == '+' or
                                                                  client_info["score"][0] == '-'):
                        value = int(client_info["score"][1:])
                        if value >= 0:
                            result = True

        except (TypeError, KeyError, ValueError):
            pass

        return result

    def start(self, mode):
        """
            In CLIENT_MODE:

                Establish a connection with the server before sending a new message.

            In SERVER_MODE:

                Start listening to the incoming messages from the clients.

        :param mode: (int) Either CLIENT_MODE or SERVER_MODE.
        :return: None
        """
        address = 'tcp://{}:{}'.format(self.ip, self.port)

        if mode == CLIENT_MODE:
            self.mode = mode
            #print("[ScoreboardWrapper][start][{}] address: {}".format("SERVER_MODE" if mode == SERVER_MODE else
            #                                                          "CLIENT_MODE", address))  # DEBUGGING
            self.instance = Proxy(address)

        elif mode == SERVER_MODE:
            self.mode = mode
            #print("[ScoreboardWrapper][start][{}] address: {}".format("SERVER_MODE" if mode == SERVER_MODE else
            #                                                          "CLIENT_MODE", address)) #DEBUGGING
            self.scoreboard = Scoreboard()
            server = Server(self, address)
            server.serve_forever()

    def reset(self):
        """

            Resets the info in the server.

        :return: None
        """
        if self.mode == SERVER_MODE:
            self.scoreboard.reset()

        elif self.mode == CLIENT_MODE:
            self.instance.reset()

    def update(self, client_info):
        """
            In CLIENT_MODE:

                Sends updated client score to the shared Scoreboard.

            In SERVER_MODE:

                Updates the client score and sends back the updated client score to the client.

        :param client_info: (dict) A JSON submitted by the client, as specified in the Code Challenge:

                Examples:

                            {"user": 123, "total": 250}
                            {"user": 456, "score": "+10"}
                            {"user": 789, "score": "-20"}

        :return: (dict) The updated client score.
        """
        if self.mode == SERVER_MODE:
            if isinstance(client_info, str):
                client_info = loads(client_info)
            self.scoreboard.update(client_info)
            client = self.scoreboard.get(client_info["user"])
            result = {"user": client.id, "total": client.score}
            result = dumps(result)

        elif self.mode == CLIENT_MODE and self.is_valid_info(client_info):
            result = self.instance.update(dumps(client_info))
            result = loads(result)

        else:
            result = {"error": "Invalid client info"}

        return result

    def top(self, top_size):
        """
            Asks the shared Scoreboard for the clients that occupy the specified number of top ranking positions
            (i.e., those with the higher score values), according to the absolute ranking.

        :param top_size: (int) Number of higher ranking positions to retrieve.
        :return: (list of dict) The clients that occupies the specified ranking positions.
        """
        if self.mode == SERVER_MODE:
            result = self.scoreboard.top(int(top_size))
            #print("\n\nSERVER.TOP[1]  top_size: {} , result: {}".format(top_size, result))

            # Serialize to stringified JSON to be sent to the client
            # From list of tuples to list of dicts
            serial_result = []
            for client in result:
                serial_result.append(client.to_json())
            result = dumps(serial_result)
            #print("\n\nSERVER.TOP[2]  top_size: {} , result: {}".format(top_size, result))

        elif self.mode == CLIENT_MODE and isinstance(top_size, int):
            result = self.instance.top(str(top_size))
            result = loads(result)

        else:
            result = {"error": "Invalid top size"}

        return result

    def relative_top(self, ranking_position, scope_size):
        """
            Asks the shared Scoreboard for the relative top (see Scoreboard.relative_top)

        :param ranking_position: (int) Ranking position to retrieve scope around. Must be a positive value, from 1 to N.
        :param scope_size: (int) Scope size (see explanation above). Must be a positive value.
        :return: (list of dict) The clients that occupies the specified ranking positions.
        """
        if self.mode == SERVER_MODE:
            result = self.scoreboard.relative_top(int(ranking_position), int(scope_size))
            #print("\n\nSERVER.RELATIVE_TOP[1]  ranking_position: {} , scope_size: {} ,result: {}".format(ranking_position,
            #                                                                                    scope_size, result))

            # Serialize to stringified JSON to be sent to the client
            # From list of tuples to list of dicts
            serial_result = []
            for client in result:
                serial_result.append(client.to_json())
            result = dumps(serial_result)
            #print("\n\nSERVER.RELATIVE_TOP[2]  ranking_position: {} , scope_size: {} ,result: {}".format(ranking_position,
            #                                                                                    scope_size, result))

        elif self.mode == CLIENT_MODE and isinstance(ranking_position, int) and isinstance(scope_size, int):
            result = self.instance.relative_top(str(ranking_position), str(scope_size))
            result = loads(result)

        else:
            result = {"error": "Invalid ranking_position, scope_size values"}

        return result

