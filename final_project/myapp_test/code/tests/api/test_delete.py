import allure
import pytest

from tests.api.base_api import ApiBaseCase


class ApiDeleteCase(ApiBaseCase):

    user = None

    @pytest.fixture(scope='function')
    def prepare(self):
        self.user = self.builder.create_fake_user()


class TestApiDeleteValid(ApiDeleteCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Delete method tests')
    @allure.story('Valid delete')
    @allure.title('Test delete status code')
    @allure.description('''
    Проверка статус кода при валидном запросе
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_delete_status(self, prepare):
        response = self.api_client.delete_user(self.user.username)
        assert response.status_code == 204

    @allure.epic('Myapp API tests')
    @allure.feature('Delete method tests')
    @allure.story('Valid delete')
    @allure.title('Test delete removes user')
    @allure.description('''
    Проверка, что пользователь удаляется из БД при валидном запросе
    * отправляет запрос
    * проверяет отсутствие пользователя
    ''')
    def test_delete_sql(self, prepare):
        username = self.user.username
        self.api_client.delete_user(username)
        self.mysql_client.expire_all()
        assert not self.mysql_client.user_exists(username)


class TestApiDeleteNotExisting(ApiDeleteCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Delete method tests')
    @allure.story('Invalid delete')
    @allure.title('Test delete not existing user')
    @allure.description('''
    Проверка статус кода, если пользователя не существует
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_delete_status(self):
        response = self.api_client.delete_user(self.faker.user_name())
        assert response.status_code == 404


class TestApiDeleteUnauthorized(ApiDeleteCase):

    authorized = False

    @allure.epic('Myapp API tests')
    @allure.feature('Delete method tests')
    @allure.story('Invalid delete')
    @allure.title('Test delete unauthorized')
    @allure.description('''
    Проверка статус кода, если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_delete_status(self, prepare):
        response = self.api_client.delete_user(self.user.username)
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Delete method tests')
    @allure.story('Invalid delete')
    @allure.title('Test delete unauthorized dont change field')
    @allure.description('''
    Проверка, что пользователь не удаляется если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет наличие пользователя
    ''')
    def test_delete_sql(self, prepare):
        username = self.user.username
        self.api_client.delete_user(username)
        self.mysql_client.expire_all()
        assert self.mysql_client.user_exists(username)


class TestApiDeleteBlocked(ApiDeleteCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Delete method tests')
    @allure.story('Invalid delete')
    @allure.title('Test delete blocked')
    @allure.description('''
    Проверка статус кода, если запрос отправлен заблокированным пользователем 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_delete_status(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        response = self.api_client.delete_user(self.user.username)
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Delete method tests')
    @allure.story('Invalid delete')
    @allure.title('Test delete blocked dont change field')
    @allure.description('''
    Проверка, что пользователь не удаляется если запрос отправлен заблокированным пользователем 
    * отправляет запрос
    * проверяет наличие пользователя
    ''')
    def test_delete_sql(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        username = self.user.username
        self.api_client.delete_user(username)
        self.mysql_client.expire_all()
        assert self.mysql_client.user_exists(username)

