import pytest

from api.client import ApiClient
from docker_client.app_mock_docker import AppMockDockerClient
from docker_client.nginx_docker import NginxDockerClient
from mysql.client import MysqlClient


def setup_db_and_user(db_name, db_host):
    mysql_client = MysqlClient('root', 'pass', db_name, db_host)
    mysql_client.recreate_db('test_qa')
    mysql_client.create_app_table()


@pytest.fixture(scope='function')
def app_mock_docker(hash_label, config, app_url, mysql_name, test_dir):
    setup_db_and_user(hash_label, mysql_name)
    app_mock_docker = AppMockDockerClient(config['tag'], hash_label, test_dir)
    proxy_docker = NginxDockerClient(config['tag'], hash_label, test_dir)
    ApiClient(app_url).wait_for_app()

    yield app_mock_docker

    proxy_docker.shutdown()
    app_mock_docker.shutdown()
