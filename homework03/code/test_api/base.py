import pytest
import credentials
from api.client import ApiClient


class ApiBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client: ApiClient, repo_root):
        self.api_client = api_client
        self.repo_root = repo_root
        self.api_client.post_login(credentials.EMAIL, credentials.PASSWORD)
