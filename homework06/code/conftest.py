import os

import pytest

from mysql.client import MysqlClient


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_PYTHON')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_PYTHON')

        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_all_tables_from_base()
        mysql_client.connection.close()
