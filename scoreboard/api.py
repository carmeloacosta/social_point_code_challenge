#!/bin/python3

"""
    HTTP RESTful API module.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return "Hello, World! [GET]"
    elif request.method == "POST":
        return "Hello, World! [POST]"


@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    if request.method == "GET":
        return "Delete {} [GET]".format(id)
    elif request.method == "POST":
        return "Hello, World! [POST]"
