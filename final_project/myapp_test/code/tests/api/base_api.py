import pytest
from docker_client.app_mock_docker import AppMockDockerClient
from api.client import ApiClient
from mysql.client import MysqlClient
from mysql.builder import MySQLBuilder


class ApiBaseCase:

    authorized = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, app_mock_docker: AppMockDockerClient, api_client: ApiClient, mysql_client: MysqlClient, faker):
        self.api_client = api_client
        self.mysql_client = mysql_client
        self.app_mock_docker = app_mock_docker

        self.faker = faker
        self.builder = MySQLBuilder(self.mysql_client, self.faker)

        if self.authorized:
            self.api_user = self.builder.create_fake_user()
            self.api_client.login(self.api_user.username, self.api_user.password)
