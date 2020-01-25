#!/bin/python3

from multiprocessing import Process

import os
import sys
import signal
os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ':'+path

from conf import NUM_CLIENTS
from app import start_scoreboard_client, start_scoreboard_server
from constants import DEFAULT_IP, DEFAULT_PORT, CLIENT_MODE, SERVER_MODE, DEBUG

process_list = []


def handler_stop_signals(signum, frame):
    """
        Handles stop signals to exit nicely

    :return: None
    """
    global process_list

    for process in process_list:
        process.terminate()

    sys.exit(0)


def main():

    global process_list

    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)

    initial_port = server_port = DEFAULT_PORT + NUM_CLIENTS
    print("Starting SCOREBOARD with {} clients, starting at {}:{} ...".format(NUM_CLIENTS, DEFAULT_IP, DEFAULT_PORT))
    #import ipdb; ipdb.set_trace()  # DEBUGGING
    server_app = Process(target=start_scoreboard_server, args=(server_port, DEFAULT_IP, DEBUG))
    server_app.start()
    process_list.append(server_app)

    for _ in range(NUM_CLIENTS-1):
        initial_port -= 1
        new_client_app = Process(target=start_scoreboard_client, args=(initial_port, DEFAULT_IP, server_port,
                                                                       DEFAULT_IP, DEBUG))
        new_client_app.start()
        process_list.append(new_client_app)

    # LAUNCH LAST CLIENT IN THIS PROCESS
    initial_port -= 1
    print("Listening ...\n")
    start_scoreboard_client(initial_port, "192.168.99.1", server_port, DEFAULT_IP, DEBUG)


if __name__ == '__main__':
    main()
