import pytest
from tests.base_test import BaseTest


class TestApp(BaseTest):

    username = None

    @pytest.fixture(scope='function', autouse=True)
    def prepare(self):
        self.username = self.faker.first_name()

    @pytest.fixture(scope='function', autouse=True)
    def teardown(self):
        yield
        self.app_data.pop(self.username, None)

    def test_add_get_user(self):

        status, data = self.app_client.add_user(self.username)
        user_id = data['user_id']

        assert status['code'] == 201

        status, data = self.app_client.get_user(self.username)
        user_id_from_get = data['user_id']

        assert status['code'] == 200
        assert user_id == user_id_from_get

    def test_get_non_existent_user(self):

        status, _ = self.app_client.get_user(self.username)
        assert status['code'] == 404

    def test_add_existent_user(self):

        self.app_client.add_user(self.username)
        status, _ = self.app_client.add_user(self.username)
        assert status['code'] == 400

    def test_get_age(self):

        self.app_client.add_user(self.username)

        status, data = self.app_client.get_user(self.username)

        assert status['code'] == 200
        assert isinstance(data['age'], int)
        assert 0 <= data['age'] <= 100

    def test_has_surname(self):

        surname = 'Zaitceva'
        self.surname_data[self.username] = surname

        self.app_client.add_user(self.username)

        status, data = self.app_client.get_user(self.username)

        assert status['code'] == 200
        assert data['surname'] == 'Zaitceva'
        self.surname_data.pop(self.username)

    def test_has_not_surname(self):

        self.app_client.add_user(self.username)

        status, data = self.app_client.get_user(self.username)
        assert status['code'] == 200
        assert data['surname'] is None
