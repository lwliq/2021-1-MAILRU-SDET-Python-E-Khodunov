import allure
import pytest


from tests.ui.base_ui import UIBaseCase
from ui.pages.registration_page import RegistrationPage


class UIRegistrationPageCase(UIBaseCase):
    authorized = False

    def additional_setup(self, request):
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')


class TestUIRegistrationValid(UIRegistrationPageCase):

    @pytest.fixture(scope='function')
    def prepare(self):
        self.user = {
            'username': self.faker.user_name()[:16],
            'email': self.faker.email()[:64],
            'password': self.faker.password()[:255],
        }

        self.registration_page.enter_all_creds_dict(self.user)

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Valid registration tests')
    @allure.title('Test redirect to /welcome after valid registration')
    @allure.description('''
    Проверка редиректа при успешной регистрации
    * вносит во все поля валидные данные
    * проверяет редирект на /welcome
    ''')
    def test_registration_web(self, prepare):
        welcome_page = self.registration_page.submit_and_go_to_welcome_page()
        assert self.driver.current_url == welcome_page.url

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Valid registration tests')
    @allure.title('Test change of access field on valid login')
    @allure.description('''
    Проверка установки поля access=1 после валидной регистрации
    * вносит во все поля валидные данные
    * проверяет, что поле access=1
    ''')
    def test_registration_sql_access(self, prepare):
        self.registration_page.submit_and_go_to_welcome_page()
        self.mysql_client.expire_all()
        assert self.mysql_client.get_user(self.user['username']).access == 1

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Valid registration tests')
    @allure.title('Test change of active field on valid login')
    @allure.description('''
    Проверка установки поля active=1 после валидной регистрации
    * вносит во все поля валидные данные
    * проверяет, что поле active=1
    ''')
    def test_registration_sql_active(self, prepare):
        self.registration_page.submit_and_go_to_welcome_page()
        self.mysql_client.expire_all()
        assert self.mysql_client.get_user(self.user['username']).active == 1

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Valid registration tests')
    @allure.title('Test change of start_active_time field on valid login')
    @allure.description('''
    Проверка установки поля start_active_time=1 после валидной регистрации
    * вносит во все поля валидные данные
    * проверяет, что поле start_active_time=1
    ''')
    def test_registration_sql_start_time(self, prepare):
        self.registration_page.submit_and_go_to_welcome_page()
        self.mysql_client.expire_all()
        assert self.mysql_client.get_user(self.user['username']).start_active_time is not None


class TestUIRegistrationValidation(UIRegistrationPageCase):
    @pytest.fixture(scope='function')
    def prepare(self):
        self.user = {
            'username': self.faker.user_name()[:16],
            'email': self.faker.email()[:64],
            'password': 'test',
            'confirm': 'test',
        }

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Invalid registration tests')
    @allure.title('Test HTML validation of form fields')
    @allure.description('''
    Проверка HTML валидации каждого поля формы
    * не вносит одно из полей
    * проверяет наличие сообщения о валидации
    ''')
    @pytest.mark.parametrize('field', [
        'username', 'email', 'password', 'confirm'
    ])
    def test_registration_validation_empty(self, prepare, field):
        self.user[field] = ''
        self.registration_page.enter_all_creds_dict(self.user)
        self.registration_page.enter_confirm(self.user['confirm'])

        self.registration_page.click_submit()

        assert self.registration_page.get_validation_messages()[field] is not None

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Invalid registration tests')
    @allure.title('Test HTML validation of terms checkbox')
    @allure.description('''
    Проверка HTML валидации каждого чекбокса
    * вносит данные во все поля, не проставляя чекбокс
    * проверяет наличие сообщения о валидации
    ''')
    def test_registration_validation_term(self, prepare):
        self.registration_page.enter_all_creds_dict(self.user, term=False)

        self.registration_page.click_submit()

        assert len(self.registration_page.get_validation_messages()['term']) > 0

    # @pytest.mark.parametrize('field, char_length', [
    #     ('username', 5),
    #     ('username', 17),
    #     ('email', 5),
    #     ('email', 65),
    #     ('password', 256)
    # ])
    # def test_registration_alert_type(self, prepare, field, char_length):
    #     self.user.update({field: 't' * char_length})
    #     self.registration_page.enter_all_creds_dict(self.user)
    #     self.registration_page.click_submit()
    #     assert self.registration_page.get_alert_type() == 'danger'

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Invalid registration tests')
    @allure.title('Test validation of form fields')
    @allure.description('''
    Проверка появления алерта с соответствующим текстом
    при вводе не валидных данных
    * вносит данные в поля
    * проверяет текст алерта на соответствие заданному в параметре
    ''')
    @pytest.mark.parametrize('field, char_length, expected_result', [
        ('username', 5, 'Incorrect username length'),
        ('username', 17, 'Incorrect username length'),
        ('email', 5, 'Incorrect email length'),
        ('email', 65, 'Incorrect email length'),
        ('password', 256, 'Incorrect password length')
    ])
    def test_registration_alert_text_len(self, prepare, field, char_length, expected_result):
        self.user.update({field: 't' * char_length})
        self.registration_page.enter_all_creds_dict(self.user)
        self.registration_page.click_submit()
        assert self.registration_page.get_alert_message() == expected_result

    # def test_registration_alert_type_passwords_dont_match(self, prepare):
    #     self.registration_page.enter_all_creds_dict(self.user)
    #     self.registration_page.enter_confirm('t')
    #     self.registration_page.click_submit()
    #     assert self.registration_page.get_alert_type() == 'danger'

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Invalid registration tests')
    @allure.title('Test validation of passwords match')
    @allure.description('''
    Проверка появления алерта с соответствующим текстом
    при вводе разных паролей
    * вносит данные в поля
    * проверяет текст алерта на соответствие 
    ''')
    def test_registration_alert_text_passwords_dont_match(self, prepare):
        self.registration_page.enter_all_creds_dict(self.user)
        self.registration_page.enter_confirm('t')
        self.registration_page.click_submit()
        assert self.registration_page.get_alert_message() == 'Passwords must match'

    # def test_registration_alert_type_multiple_wrong(self, prepare):
    #     self.user.update({
    #         'username': 't' * 5,
    #         'email': 't' * 5
    #     })
    #     self.registration_page.enter_all_creds_dict(self.user)
    #     self.registration_page.click_submit()
    #     assert self.registration_page.get_alert_type() == 'danger'

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Invalid registration tests')
    @allure.title('Test validation of multiple errors')
    @allure.description('''
    Проверка появления алерта с соответствующим текстом
    при не валидном вводе нескольких полей
    * вносит данные в поля
    * проверяет текст алерта на соответствие 
    ''')
    def test_registration_alert_text_multiple_wrong(self, prepare):
        self.user.update({
            'username': 't' * 5,
            'email': 't' * 5
        })
        self.registration_page.enter_all_creds_dict(self.user)
        self.registration_page.click_submit()
        assert self.registration_page.get_alert_message() == 'Incorrect username and email length'


class TestUIRegistrationExisting(UIRegistrationPageCase):

    @pytest.fixture(scope='function')
    def prepare(self):

        self.user = self.builder.create_fake_user()

        self.user_dict = {
            'username': self.faker.user_name()[:16],
            'password': self.faker.password()[:255],
            'email': self.faker.email()[:64]
        }

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Invalid registration tests')
    @allure.title('Test registration with existing username')
    @allure.description('''
    Проверка появления алерта с соответствующим текстом
    при регистрации с уже существующим именем
    * вносит данные в поля, username берем у уже существующего пользователя
    * проверяет текст алерта на соответствие 
    ''')
    def test_registration_username(self, prepare):
        self.user_dict.update({'username': self.user.username})
        self.registration_page.enter_all_creds_dict(self.user_dict)
        self.registration_page.click_submit()
        assert self.registration_page.get_alert_message() == 'User already exist'

    @allure.epic('Myapp UI tests')
    @allure.feature('Registration page tests')
    @allure.story('Invalid registration tests')
    @allure.title('Test registration with existing email')
    @allure.description('''
    Проверка появления алерта с соответствующим текстом
    при регистрации с уже существующим email
    * вносит данные в поля, username берем у уже существующего пользователя
    * проверяет текст алерта на соответствие 
    ''')
    def test_registration_email(self, prepare):
        self.user_dict.update({'email': self.user.email})
        self.registration_page.enter_all_creds_dict(self.user_dict)
        self.registration_page.click_submit()
        assert self.registration_page.get_alert_message() == 'User already exist'
