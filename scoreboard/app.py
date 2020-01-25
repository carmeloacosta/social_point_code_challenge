#!/bin/python3

"""
    Scoreboard Application module. Allows to share an Scoreboard with multiple simultaneous client requests.
"""

import os
os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path

from api import get_api
from scoreboard_wrapper import ScoreboardWrapper
from constants import DEFAULT_IP, DEFAULT_PORT, CLIENT_MODE, SERVER_MODE


def start_scoreboard_server(port=DEFAULT_PORT, ip=DEFAULT_IP, debug_mode=True):
    """
        Starts an wrapped Scoreboard acting as a server.

        If debug_mode returns an initialized, but not started, wrapped Scoreboard acting as a server.

    :param port:
    :param ip:
    :param debug_mode:
    :return:
    """
    #print("\n\n\n[APP][start_scoreboard_server] port={}, ip={}, debug_mode={}".format(port, ip, debug_mode)) #DEBUGGING
    server = ScoreboardWrapper(port, ip)

    if not debug_mode:
        server.start(SERVER_MODE)
    else:
        return server


def start_scoreboard_client(api_port=DEFAULT_PORT, api_ip=DEFAULT_IP, server_port=DEFAULT_PORT+1,
                            server_ip=DEFAULT_IP, debug_mode=True):
    """
        Starts an wrapped Scoreboard acting as a client, connected with an HTTP API and with the server.

        If debug_mode returns an initialized HTTP API, but not started, connected with the wrapped Scoreboard acting
            as a client.

    :param port:
    :param ip:
    :param debug_mode:
    :return:
    """
    print("\n\n\n[APP][start_scoreboard_client] api_port={}, api_ip={}, server_port={}, server_ip={}, debug_mode={}"
          "".format(api_port, api_ip, server_port, server_ip, debug_mode))  # DEBUGGING
    client = ScoreboardWrapper(server_port, server_ip)
    client.start(CLIENT_MODE)

    api = get_api(client)

    if not debug_mode:
        print("Starting API in {}:{}".format(api_ip, api_port)) #DEBUGGING
        api.run(host=api_ip, port=api_port)
    else:
        return api
