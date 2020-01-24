#!/bin/python3

"""
    HTTP RESTful API module.
"""

# Add Flask app
from flask import Flask, request
app = Flask(__name__)

# Add logger
import logging
logger = logging.getLogger(__name__)

from json import dumps, loads


# Define API on Flask app
@app.route("/score", methods=["PUT"])
def score():
    if request.method == "PUT":
        user_msg = loads(request.data.decode())
        #print("[/score] user_msg: {}".format(user_msg)) #DEBUGGING
        response = app.scoreboard.update(user_msg)
        return dumps(response)


@app.route("/top/<int:top_size>", methods=["GET"])
def top(top_size):
    if request.method == "GET":
        #print("[/top/{}] ".format(top_size)) #DEBUGGING
        response = app.scoreboard.top(top_size)
        return dumps(response)


@app.route("/top/<int:ranking_position>/<int:scope_size>", methods=["GET"])
def relative_top(ranking_position, scope_size):
    if request.method == "GET":
        #print("[/top/{}/{}] ".format(ranking_position, scope_size)) #DEBUGGING
        response = app.scoreboard.relative_top(ranking_position, scope_size)
        return dumps(response)


def get_api(scoreboard_wrapper):
    """
        Returns an initialized HTTP RESTful API

    :param scoreboard_wrapper: (ScoreboardWrapper) Give access to the shared Scoreboard.
    :return: (Flask) API to communicate with clients.
    """
    # Add a wrapper to get access to the scoreboard
    setattr(app, "scoreboard", scoreboard_wrapper)
    return app
