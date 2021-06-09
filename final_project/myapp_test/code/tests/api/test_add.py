import allure
import pytest


from tests.api.base_api import ApiBaseCase


class ApiAddCase(ApiBaseCase):

    user = None
    user_dict = None
    same_username = False
    same_email = False

    @pytest.fixture(scope='function')
    def prepare(self):
        if self.same_username or self.same_email:
            self.user = self.builder.create_fake_user()

        self.user_dict = {
            'username': self.user.username if self.same_username else self.faker.user_name()[:16],
            'password': self.faker.password()[:255],
            'email': self.user.email if self.same_email else self.faker.email()[:64]
        }


class TestApiAddValid(ApiAddCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Valid add')
    @allure.title('Test add status code')
    @allure.description('''
    Проверка статус кода при валидном запросе
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_add_user_status(self, prepare):
        response = self.api_client.add_user(self.user_dict)
        assert response.status_code == 201

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Valid add')
    @allure.title('Test add adds user')
    @allure.description('''
    Проверка, что пользователь добавляется в БД при валидном запросе
    * отправляет запрос
    * проверяет  наличие пользователя
    ''')
    def test_add_user_sql(self, prepare):
        self.api_client.add_user(self.user_dict)
        self.mysql_client.expire_all()
        assert self.mysql_client.user_exists(self.user_dict['username'])

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Valid add')
    @allure.title('Test add adds user access')
    @allure.description('''
    Проверка, что пользователь добавляется с access=1
    * отправляет запрос
    * проверяет  что access=1
    ''')
    def test_add_user_sql_access(self, prepare):
        self.api_client.add_user(self.user_dict)
        self.mysql_client.expire_all()
        assert self.mysql_client.get_user(self.user_dict['username']).access == 1


class TestApiAddExistingUsername(ApiAddCase):

    same_username = True

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test add existing username')
    @allure.description('''
    Проверка, корректного статус кода при попытке добавить пользователя с уже 
    существующим username
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_add_status(self, prepare):
        response = self.api_client.add_user(self.user_dict)
        assert response.status_code == 304


class TestApiAddExistingEmail(ApiAddCase):

    same_email = True

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test add existing email')
    @allure.description('''
    Проверка, корректного статус кода при попытке добавить пользователя с уже 
    существующим email
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_add_status(self, prepare):
        response = self.api_client.add_user(self.user_dict)
        assert response.status_code == 304


FIELD_LEN = [
        ('username', 17),
        ('username', 5),
        ('email', 65),
        ('email', 5),
        ('password', 256)
    ]


class TestApiAddInvalidCreds(ApiAddCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test invalid length status')
    @allure.description('''
    Проверка, корректного статус кода при попытке добавить пользователя с невалидным
    полем 
    * отправляет запрос
    * проверяет статус код
    ''')
    @pytest.mark.parametrize('field,char_count', FIELD_LEN)
    def test_add_invalid_length_status(self, prepare, field, char_count):
        self.user_dict.update({field: 't' * char_count})
        response = self.api_client.add_user(self.user_dict)
        assert response.status_code == 400

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test invalid length dont add')
    @allure.description('''
    Проверка, что пользователь не создается с не валидным  
    полем 
    * отправляет запрос
    * проверяет отсутствие пользователя в БД
    ''')
    @pytest.mark.parametrize('field,char_count', FIELD_LEN)
    def test_add_invalid_length_sql(self, prepare, field, char_count):
        self.user_dict.update({field: 't' * char_count})
        self.api_client.add_user(self.user_dict)
        self.mysql_client.expire_all()
        assert not self.mysql_client.user_exists(self.user_dict['username'])

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test not email')
    @allure.description('''
    Проверка, что пользователь не создается с некорректным email
    * отправляет запрос
    * проверяет отсутствие пользователя в БД
    ''')
    def test_add_not_email(self, prepare):
        self.user_dict.update({'email': 't' * 64})
        self.api_client.add_user(self.user_dict)
        self.mysql_client.expire_all()
        assert not self.mysql_client.user_exists(self.user_dict['username'])


class TestApiAddUnauthorized(ApiAddCase):

    authorized = False

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test add unauthorized')
    @allure.description('''
    Проверка статус кода, если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_add_user_status(self, prepare):
        response = self.api_client.add_user(self.user_dict)
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test add unauthorized dont add')
    @allure.description('''
    Проверка, что пользователь не добавляется если запрос отправлен без авторизации 
    * отправляет запрос
    * проверяет отсутствие пользователя
    ''')
    def test_add_user_sql(self, prepare):
        self.api_client.add_user(self.user_dict)
        self.mysql_client.expire_all()
        assert not self.mysql_client.user_exists(self.user_dict['username'])


class TestApiAddBlocked(ApiAddCase):

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test add unauthorized')
    @allure.description('''
    Проверка статус кода, если запрос отправлен заблокированным пользователем
    * отправляет запрос
    * проверяет статус код
    ''')
    def test_add_user_status(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        response = self.api_client.add_user(self.user_dict)
        assert response.status_code == 401

    @allure.epic('Myapp API tests')
    @allure.feature('Add method tests')
    @allure.story('Invalid add')
    @allure.title('Test add blocked')
    @allure.description('''
    Проверка, что пользователь не добавляется если запрос отправлен от заблокированного пользователя
    * отправляет запрос
    * проверяет отсутствие пользователя
    ''')
    def test_add_user_sql(self, prepare):
        self.api_user.access = 0
        self.mysql_client.session.commit()
        self.api_client.add_user(self.user_dict)
        self.mysql_client.expire_all()
        assert not self.mysql_client.user_exists(self.user_dict['username'])
