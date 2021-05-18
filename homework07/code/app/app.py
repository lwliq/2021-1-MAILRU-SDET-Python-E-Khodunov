import json
import logging

import requests
from flask import Flask, request, jsonify

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
app_data = {}
user_id_seq = 1

STUB_HOST = '127.0.0.1'
STUB_PORT = '8000'

MOCK_HOST = '127.0.0.1'
MOCK_PORT = '8001'


@app.route('/add_user', methods=['POST'])
def create_user():
    global user_id_seq

    user_name = json.loads(request.data)['name']
    if user_name not in app_data:
        app_data[user_name] = user_id_seq

        data = {'user_id': user_id_seq}
        user_id_seq += 1
        return jsonify(data), 201
    else:
        return jsonify(f'User name {user_name} already exists: id {app_data[user_name]}'), 400


@app.route('/get_user/<name>', methods=['GET'])
def get_user_id_by_name(name):
    if user_id := app_data.get(name):

        age = None
        try:
            age = requests.get(f'http://{STUB_HOST}:{STUB_PORT}/get_age/{name}').json()
        except Exception as e:
            print(f'Unable to get age from external system:\n{e}')

        surname = None
        try:
            resp = requests.get(f'http://{MOCK_HOST}:{MOCK_PORT}/get_surname/{name}')
            if resp.status_code == 200:
                surname = resp.json()

        except Exception as e:
            print(f'Unable to get surname from external system:\n{e}')

        data = {'user_id': user_id,
                'age': age,
                'surname': surname
                }

        return jsonify(data), 200
    else:
        return jsonify(f'User name {name} not found'), 404


def shutdown_server():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return jsonify('OK, Exiting.'), 200
