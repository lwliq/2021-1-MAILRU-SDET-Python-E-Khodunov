import pytest

from mysql.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_name(config):
    return f'{config["tag"]}_mysql'


@pytest.fixture(scope='function')
def mysql_client(hash_label, mysql_name):
    mysql_client = MysqlClient('root', 'pass', hash_label, mysql_name)
    mysql_client.connect()

    yield mysql_client

    mysql_client.close()