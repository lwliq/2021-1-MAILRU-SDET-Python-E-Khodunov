import time

import allure
import pytest


from tests.ui.base_ui import UIBaseCase
from ui.pages.login_page import LoginPage


class UILoginPageCase(UIBaseCase):
    authorized = False

    def additional_setup(self, request):
        self.login_page: LoginPage = request.getfixturevalue('login_page')


class TestUILoginValid(UILoginPageCase):

    @pytest.fixture(scope='function')
    def prepare(self):
        self.user = self.builder.create_fake_user(access=True, active=False)
        self.login_page.enter_username(self.user.username)
        self.login_page.enter_password(self.user.password)

    @allure.epic('Myapp UI tests')
    @allure.feature('Login page tests')
    @allure.story('Valid login tests')
    @allure.title('Test redirect to /welcome on valid login')
    @allure.description('''
    Проверка редиректа при вводе верных данных
    * вносит данные уже созданного юзера
    * подтверждает ввод
    * проверяет текущий url
    ''')
    def test_login_web(self, prepare):
        welcome_page = self.login_page.submit_and_go_to_welcome_page()
        assert self.driver.current_url == welcome_page.url

    @allure.epic('Myapp UI tests')
    @allure.feature('Login page tests')
    @allure.story('Valid login tests')
    @allure.title('Test change of active field on valid login')
    @allure.description('''
    Проверка установки active пользователя в 1 после
    успешной авторизации
    * вносит данные уже созданного юзера
    * подтверждает ввод
    * проверяет текущее знчение active
    ''')
    def test_login_active(self, prepare):
        self.login_page.submit_and_go_to_welcome_page()
        self.mysql_client.expire_all()
        assert self.user.active == 1

    @allure.epic('Myapp UI tests')
    @allure.feature('Login page tests')
    @allure.story('Valid login tests')
    @allure.title('Test change of start_active_time field on valid login')
    @allure.description('''
    Проверка изменения поля start_active_time после
    успешной авторизации
    * вносит данные уже созданного юзера
    * запоминает текущий start_active_time
    * подтверждает ввод
    * сравнивает записанный и новый start_active_time
    ''')
    def test_login_active_time(self, prepare):
        active_time = self.user.start_active_time
        self.login_page.submit_and_go_to_welcome_page()
        self.mysql_client.expire_all()
        assert self.user.start_active_time != active_time


class TestUILoginValidation(UILoginPageCase):

    @allure.epic('Myapp UI tests')
    @allure.feature('Login page tests')
    @allure.story('Invalid login tests')
    @allure.title('Test HTML validation of form fields')
    @allure.description('''
    Проверка HTML валидации каждого поля формы
    * не вносит необходимое поле
    * проверяет наличие сообщения о валидации
    ''')
    @pytest.mark.parametrize('username, password, result', [
        ('', 'pass', 'username'),
        ('testtest', '', 'password')
    ])
    def test_login_validation_empty(self, username, password, result):
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_submit()

        assert self.login_page.get_validation_messages()[result] is not None

    # @pytest.mark.parametrize('char_length, expected_result', [
    #     (5, 'danger'),
    #     (17, 'danger'),
    #     (8, 'warning')
    # ])
    # def test_login_alert_type(self, char_length, expected_result):
    #     self.login_page.enter_password('1')
    #     self.login_page.enter_username('t' * char_length)
    #
    #     self.login_page.click_submit()
    #
    #     assert self.login_page.get_alert_type() == expected_result

    @allure.epic('Myapp UI tests')
    @allure.feature('Login page tests')
    @allure.story('Invalid login tests')
    @allure.title('Test validation of form fields')
    @allure.description('''
    Проверка появления алерта с соответствующим текстом
    при вводе не валидных данных
    * вносит данные в поля
    * проверяет текст алерта на соответствие значению из параметра
    ''')
    @pytest.mark.parametrize('char_length, expected_result', [
        (5, 'Incorrect username length'),
        (17, 'Incorrect username length'),
        (8, 'Invalid username or password')
    ])
    def test_login_alert_text(self, char_length, expected_result):
        self.login_page.enter_password('1')
        self.login_page.enter_username('t' * char_length)

        self.login_page.click_submit()

        assert self.login_page.get_alert_message() == expected_result


class TestUILoginBlocked(UILoginPageCase):

    @allure.epic('Myapp UI tests')
    @allure.feature('Login page tests')
    @allure.story('Blocked User login tests')
    @allure.title('Test alert')
    @allure.description('''
    Проверка текста алерта при попытке входа пользователя с access=0
    * вносит данные в поля уже созданного юзера с access=0
    * проверяет текст алерта на соответствие
    ''')
    def test_login_alert_blocked(self):
        self.user = self.builder.create_fake_user(access=False, active=False)
        self.login_page.enter_username(self.user.username)
        self.login_page.enter_password(self.user.password)
        self.login_page.click_submit()

        assert self.login_page.get_alert_message() == 'Your account has been blocked'
