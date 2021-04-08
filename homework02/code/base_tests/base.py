import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.dashboard_page import DashboardPage
from ui.pages.login_page import LoginPage


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, repo_root):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.repo_root = repo_root

        self.login_page: LoginPage = request.getfixturevalue('login_page')

        if self.authorize:
            self.dashboard_page: DashboardPage = request.getfixturevalue('dashboard_page')

        self.logger.debug('Initial setup done!')
