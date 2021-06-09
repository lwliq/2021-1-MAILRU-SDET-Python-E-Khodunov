import allure
import pytest

from tests.api.base_api import ApiBaseCase


class ApiAcceptCase(ApiBaseCase):

    access = None
    user = None

    @pytest.fixture(scope='function')
    def prepare(self):
        self.user = self.builder.create_fake_user(access=self.access)


class TestApiAcceptValid(ApiAcceptCase):

    access = 0

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Valid accept')
    @allure.title('Test accept status code')
    @allure.description('''
    Проверка статус кода при валидном запросе
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_accept_status(self, prepare):
        response = self.api_client.accept_user(self.user.username)
        assert response.status_code == 200

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Valid accept')
    @allure.title('Test change of access field')
    @allure.description('''
    Проверка что метод изменяет поле acccess при валидном запросе
    * отправляет запрос
    * проверяет access=1
    ''')
    def test_accept_sql(self, prepare):
        self.api_client.accept_user(self.user.username)
        self.mysql_client.expire_all()
        assert self.user.access == 1


class TestApiAcceptAccepted(ApiAcceptCase):

    access = 1

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Invalid accept')
    @allure.title('Test accept accepted user')
    @allure.description('''
    Проверка статус кода, если поле не изменяет значение 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_accept_status(self, prepare):
        response = self.api_client.accept_user(self.user.username)
        assert response.status_code == 304


class TestApiAcceptNotExisting(ApiAcceptCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Invalid accept')
    @allure.title('Test accept not existing user')
    @allure.description('''
    Проверка статус кода, если пользователь не существует 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_accept_status(self):
        response = self.api_client.accept_user(self.faker.user_name())
        assert response.status_code == 404


class TestApiAcceptUnauthorized(ApiAcceptCase):

    authorized = False
    access = 0

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Invalid accept')
    @allure.title('Test accept unauthorized')
    @allure.description('''
    Проверка статус кода, если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_accept_status(self, prepare):
        response = self.api_client.accept_user(self.faker.user_name())
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Invalid accept')
    @allure.title('Test accept unauthorized dont change field')
    @allure.description('''
    Проверка, что поле не изменяется если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет значение поля
    ''')
    def test_accept_sql(self, prepare):
        self.api_client.accept_user(self.user.username)
        self.mysql_client.expire_all()
        assert self.user.access == 0


class TestApiAcceptByBlocked(ApiAcceptCase):
    access = 0

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Invalid accept')
    @allure.title('Test accept by blocked')
    @allure.description('''
    Проверка статус кода, если запрос отправлен заблокированным пользователем 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_accept_status(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        response = self.api_client.accept_user(self.faker.user_name())
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Accept method tests')
    @allure.story('Invalid accept')
    @allure.title('Test accept by blocked dont change field')
    @allure.description('''
    Проверка, что поле не изменяется если запрос отправлен заблокированным пользователем 
    * отправляет запрос
    * проверяет значение поля
    ''')
    def test_accept_sql(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        self.api_client.accept_user(self.user.username)
        self.mysql_client.expire_all()
        assert self.user.access == 0
