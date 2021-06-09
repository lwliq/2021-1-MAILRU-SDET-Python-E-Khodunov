import allure
import pytest

from tests.api.base_api import ApiBaseCase


class ApiBlockCase(ApiBaseCase):

    access = None
    user = None

    @pytest.fixture(scope='function')
    def prepare(self):
        self.user = self.builder.create_fake_user(access=self.access)


class TestApiBlockValid(ApiBlockCase):

    access = 1

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Valid block')
    @allure.title('Test block status code')
    @allure.description('''
    Проверка статус кода при валидном запросе
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_block_status(self, prepare):
        response = self.api_client.block_user(self.user.username)
        assert response.status_code == 200

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Valid block')
    @allure.title('Test block changes access field')
    @allure.description('''
    Проверка, что поле access=0 при валидном запросе
    * отправляет запрос
    * проверяет значение поля access=0
    ''')
    def test_block_sql(self, prepare):
        self.api_client.block_user(self.user.username)
        self.mysql_client.expire_all()
        assert self.user.access == 0

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Valid block')
    @allure.title('Test block changes active field')
    @allure.description('''
    Проверка, что поле active=0 при валидном запросе
    * отправляет запрос
    * проверяет значение поля active=0
    ''')
    def test_block_sql_active(self, prepare):
        self.api_client.block_user(self.user.username)
        self.mysql_client.expire_all()
        assert self.user.active == 0


class TestApiBlockBlocked(ApiBlockCase):

    access = 0

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Invalid block')
    @allure.title('Test block blocked user')
    @allure.description('''
    Проверка статус кода, если поле не изменяет значение
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_block_status(self, prepare):
        response = self.api_client.block_user(self.user.username)
        assert response.status_code == 304


class TestApiBlockNotExisting(ApiBlockCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Invalid block')
    @allure.title('Test block not existing user')
    @allure.description('''
    Проверка статус кода, если пользователь не существует 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_block_status(self):
        response = self.api_client.block_user(self.faker.user_name())
        assert response.status_code == 404


class TestApiBlockUnauthorized(ApiBlockCase):

    authorized = False
    access = 1

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Invalid block')
    @allure.title('Test block unauthorized')
    @allure.description('''
    Проверка статус кода, если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_block_status(self, prepare):
        response = self.api_client.block_user(self.faker.user_name())
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Invalid block')
    @allure.title('Test block unauthorized dont change field')
    @allure.description('''
    Проверка, что поле не изменяется если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет значение поля
    ''')
    def test_block_sql(self, prepare):
        self.api_client.accept_user(self.user.username)
        self.mysql_client.expire_all()
        assert self.user.access == 1


class TestApiBlockByBlocked(ApiBlockCase):

    access = 1

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Invalid block')
    @allure.title('Test block by blocked')
    @allure.description('''
    Проверка статус кода, если запрос отправлен заблокированным пользователем 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_block_status(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        response = self.api_client.block_user(self.faker.user_name())
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Block method tests')
    @allure.story('Invalid block')
    @allure.title('Test block by blocked dont change field')
    @allure.description('''
    Проверка, что поле не изменяется если запрос отправлен заблокированным пользователем  
    * отправляет запрос
    * проверяет значение поля
    ''')
    def test_block_sql(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        self.api_client.accept_user(self.user.username)
        self.mysql_client.expire_all()
        assert self.user.access == 1

