import pytest
from _pytest.fixtures import FixtureRequest


from docker_client.app_mock_docker import AppMockDockerClient
from api.client import ApiClient
from mysql.client import MysqlClient
from mysql.builder import MySQLBuilder
from selenium.webdriver.remote.webdriver import WebDriver


class UIBaseCase(object):

    authorized = False

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest):
        self.app_mock_docker: AppMockDockerClient = request.getfixturevalue('app_mock_docker')
        self.api_client: ApiClient = request.getfixturevalue('api_client')
        self.mysql_client: MysqlClient = request.getfixturevalue('mysql_client')

        self.driver: WebDriver = request.getfixturevalue('driver')

        self.faker = request.getfixturevalue('faker')
        self.builder = MySQLBuilder(self.mysql_client, self.faker)

        if self.authorized:
            self._login()

        self.additional_setup(request)

    def additional_setup(self, request):
        pass

    def _login(self):
        self.login_user = self.builder.create_fake_user()
        user_agent = self.driver.execute_script("return navigator.userAgent")
        self.api_client.session.headers.update({'User-Agent': user_agent})
        self.api_client.login(self.login_user.username, self.login_user.password)
        self.driver.add_cookie({'name': 'session', 'value': self.api_client.session.cookies.get('session', None)})