import time

from docker_client.app_mock_docker import AppMockDockerClient
from docker_client.mysql_docker import MySQLDockerClient
from mysql.client import MysqlClient

from mysql.builder import MySQLBuilder
from faker import Faker
from api.client import ApiClient

mysql_docker = MySQLDockerClient('mysql_testing', '3333')
mysql_client = MysqlClient('root', 'pass', 'testing', '3333')
mysql_client.recreate_db('test_qa')
mysql_client.create_app_table()
print('DB started')

app_mock_docker = AppMockDockerClient('testing', '9999', 'mysql_testing')
api_client = ApiClient(f'http://localhost:9999/')
api_client.wait_for_app()
print('App started')


try:
    while True:
        pass
except KeyboardInterrupt:
    pass


app_mock_docker.shutdown()
mysql_docker.shutdown()




