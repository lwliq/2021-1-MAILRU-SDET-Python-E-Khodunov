from time import time
import pytest
from tests.base_test import BaseTest


class TestMock(BaseTest):

    username = None

    @pytest.fixture(scope='function', autouse=True)
    def prepare(self):
        self.username = self.faker.first_name()

    @pytest.fixture(scope='function', autouse=True)
    def teardown(self):
        yield
        self.surname_data.pop(self.username, None)

    def test_get_existing_surname(self):

        surname = 'testtest'
        self.surname_data[self.username] = surname

        status, surname_from_mock = self.mock_client.get_surname(self.username)

        assert status['code'] == 200
        assert surname == surname_from_mock

    def test_get_not_existing_surname(self):

        status, _ = self.mock_client.get_surname(self.username)

        assert status['code'] == 404

    def test_update_existing_surname(self):

        surname = 'testtest'
        self.surname_data[self.username] = surname

        new_surname = 'testtesttest'
        status, _ = self.mock_client.update_surname(self.username, new_surname)

        assert status['code'] == 201
        assert self.surname_data[self.username] == new_surname

    def test_update_not_existing_surname(self):

        surname = 'testtest'
        status, _ = self.mock_client.update_surname(self.username, surname)

        assert status['code'] == 404

    def test_delete_existing_surname(self):

        surname = 'testtest'
        self.surname_data[self.username] = surname

        status, _ = self.mock_client.delete_surname(self.username)

        assert status['code'] == 200
        assert self.username not in self.surname_data.keys()

    def test_delete_not_existing_surname(self):

        status, _ = self.mock_client.delete_surname(self.username)

        assert status['code'] == 404
