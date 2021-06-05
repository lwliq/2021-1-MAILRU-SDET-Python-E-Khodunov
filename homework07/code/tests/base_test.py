import pytest
from _pytest.fixtures import FixtureRequest
from faker import Faker

from http_client.app_client import AppClient
from http_client.mock_client import MockClient


class BaseTest:

    faker = Faker()

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, app_client: AppClient, mock_client: MockClient, request: FixtureRequest):
        self.app_client = app_client
        self.mock_client = mock_client

        self.app_data: dict = request.config.app_data
        self.surname_data: dict = request.config.surname_data
