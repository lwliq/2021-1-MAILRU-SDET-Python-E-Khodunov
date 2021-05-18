import os
import random

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/get_age/<name>', methods=['GET'])
def get_user_id_by_name(name):
    return jsonify(random.randint(0, 100)), 200


def shutdown_server():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return jsonify('OK, Exiting.'), 200
