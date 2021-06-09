import logging
import hashlib
import http.client

from url_normalize import url_normalize
from docker_client.mysql_docker import MySQLDockerClient

from mysql.fixtures import *
from api.fixtures import *
from ui.fixtures import *
from docker_client.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--tag', default='myapp')
    parser.addoption('--vnc', action='store_true', default=False)


@pytest.fixture(scope='session')
def config(request):
    tag = request.config.getoption('--tag')
    selenoid = f'http://{tag}_selenoid:4444'
    vnc = request.config.getoption('--vnc')
    return {'tag': tag, 'selenoid': selenoid, 'vnc': vnc}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function')
def hash_label(current_test_name, config):
    hash_obj = hashlib.sha1((current_test_name + config['tag']).encode('utf-8'))
    return f'test_{hash_obj.hexdigest()[:15]}'


@pytest.fixture(scope='function')
def app_url(hash_label):
    return url_normalize(f'http://proxy_{hash_label}/')


@pytest.fixture(scope='function')
def current_test_name(request):
    return '_'.join(request._pyfuncitem.nodeid.split('::')[-2:])


@pytest.fixture(scope='function')
def test_dir(request, hash_label):
    test_dir = os.path.join(request.config.base_test_dir, hash_label)
    os.makedirs(test_dir)
    return test_dir


def pytest_configure(config):
    repo_root = os.path.abspath(os.path.join(__file__, os.pardir))
    base_test_dir = os.path.join(repo_root, 'tmp', 'tests')

    if not hasattr(config, 'workerinput'):
        config.mysql_docker = MySQLDockerClient(config.getoption('--tag'))

        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        config.mysql_docker.shutdown()


def create_logger(log_name, log_file, log_formatter=None, log_level=logging.INFO):
    if log_formatter is None:
        log_formatter = logging.Formatter('%(asctime)s - %(message)s')

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger(log_name)
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    return log


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    loggers = []

    test_log_file = os.path.join(test_dir, 'test.log')
    loggers.append(create_logger('test', test_log_file))
    api_log_file = os.path.join(test_dir, 'api_client.log')
    loggers.append(create_logger('api_client', api_log_file, log_level=logging.DEBUG))
    mysql_log_file = os.path.join(test_dir, 'mysql_client.log')
    loggers.append(create_logger('sqlalchemy.engine', mysql_log_file))

    yield loggers

    for logger in loggers:
        for handler in logger.handlers:
            handler.close()

    with open(test_log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)
    with open(api_log_file, 'r') as f:
        allure.attach(f.read(), 'api_client.log', attachment_type=allure.attachment_type.TEXT)
    with open(mysql_log_file, 'r') as f:
        allure.attach(f.read(), 'mysql_client.log', attachment_type=allure.attachment_type.TEXT)
