
import threading

from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

SURNAME_DATA = {}


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify(surname), 200
    else:
        return jsonify(f'Surname for user {name} not found'), 404


@app.route('/update_surname/<name>', methods=['PUT'])
def update_user_surname(name):
    if SURNAME_DATA.get(name):
        if surname := request.json['surname']:
            SURNAME_DATA[name] = surname
            return jsonify(f'Successfully updated surname to {surname} of user {name}'), 200
        else:
            return jsonify(f'Bad request'), 400
    else:
        return jsonify(f'Surname for user {name} not found'), 404


@app.route('/delete_surname/<name>', methods=['DELETE'])
def delete_user_surname(name):
    if SURNAME_DATA.pop(name, None):
        return jsonify(f'Successfully deleted surname of user {name}'), 200
    else:
        return jsonify(f'Surname for user {name} not found'), 404


def shutdown_server():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return jsonify('OK, Exiting.'), 200

