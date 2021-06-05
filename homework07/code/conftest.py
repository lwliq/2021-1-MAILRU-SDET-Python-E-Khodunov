import logging
import os
import shutil
import threading
from http_client.base_client import BaseHttpClient
from stub import flask_stub
from utils.decorators import wait
import pytest
from mock import mock
from app import app
import settings

from http_client.app_client import AppClient
from http_client.mock_client import MockClient

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))  # code


def run_flask_server(target, kwargs):
    server = threading.Thread(target=target.run, kwargs=kwargs)
    server.start()

    wait(
        method=BaseHttpClient(kwargs['host'], kwargs['port']).try_connect,
        error=ConnectionRefusedError,
        check=False,
        timeout=5,
        interval=0.1
    )

    return server


@pytest.fixture(scope='function')
def app_client():
    return AppClient(settings.APP_HOST, settings.APP_PORT)


@pytest.fixture(scope='function')
def mock_client():
    return MockClient(settings.MOCK_HOST, settings.MOCK_PORT)


def start_servers():

    run_flask_server(
        target=mock.app,
        kwargs={
            'host': settings.MOCK_HOST,
            'port': settings.MOCK_PORT
        }
    )

    run_flask_server(
        target=flask_stub.app,
        kwargs={
            'host': settings.STUB_HOST,
            'port': settings.STUB_PORT
        }

    )

    app.STUB_HOST = settings.STUB_HOST
    app.STUB_PORT = settings.STUB_PORT
    app.MOCK_HOST = settings.MOCK_HOST
    app.MOCK_PORT = settings.MOCK_PORT
    run_flask_server(
        target=app.app,
        kwargs={
            'host': settings.APP_HOST,
            'port': settings.APP_PORT,
        }
    )


def pytest_configure(config):
    base_test_dir = os.path.join(repo_root, 'tmp', 'tests')

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

        start_servers()

    config.app_data = app.app_data
    config.surname_data = mock.SURNAME_DATA
    config.base_test_dir = base_test_dir


def pytest_unconfigure():
    BaseHttpClient(settings.APP_HOST, settings.APP_PORT).shutdown_server()
    BaseHttpClient(settings.STUB_HOST, settings.STUB_PORT).shutdown_server()
    BaseHttpClient(settings.MOCK_HOST, settings.MOCK_PORT).shutdown_server()


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


def set_logger_options(log, log_file, log_formatter, log_level):
    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir):

    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s%(message)s')
    log_file = os.path.join(test_dir, 'client.log')
    log = logging.getLogger('client')
    set_logger_options(log, log_file, log_formatter, logging.INFO)

    yield

    for handler in log.handlers:
        handler.close()
