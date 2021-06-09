import pytest

from api.client import ApiClient


@pytest.fixture(scope='function')
def api_client(app_url):
    return ApiClient(app_url)
