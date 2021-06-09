import time

import allure
import pytest
from selenium.common.exceptions import NoSuchElementException

from tests.ui.base_ui import UIBaseCase
from ui.pages.registration_page import RegistrationPage
from ui.pages.welcome_page import WelcomePage


class UIWelcomePageCase(UIBaseCase):
    authorized = True

    def additional_setup(self, request):
        self.welcome_page: WelcomePage = request.getfixturevalue('welcome_page')

    def switch_tab(self):
        current_tab = self.driver.current_window_handle
        for tab in self.driver.window_handles:
            if current_tab != tab:
                self.driver.switch_to.window(tab)


class TestUIWelcomeContent(UIWelcomePageCase):

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct content block')
    @allure.title('Test content urls')
    @allure.description('''
    Проверка редиректа на правильные страницы
    * нажимает на необходимый элемент
    * проверяет открытие верного url
    ''')
    @pytest.mark.parametrize('link, expected_url_entry', [
        ('What is an API?', 'API'),
        ('Future of internet', 'future'),
        ('Lets talk about SMTP?', 'SMTP'),
    ])
    def test_content_links(self, link, expected_url_entry):
        self.welcome_page.click_content_link(link)
        self.switch_tab()
        assert expected_url_entry in self.driver.current_url

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct content block')
    @allure.title('Test python quote')
    @allure.description('''
    Проверка что на страницу выводится цитата
    * проверяет наличие текста в блоке с цитатой
    ''')
    def test_python_quote(self):
        assert len(self.welcome_page.get_python_quote_text()) > 0


class TestUIWelcomeLoginControl(UIWelcomePageCase):

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct login-control block')
    @allure.title('Test username')
    @allure.description('''
    Проверка, что на страницу выводится корректный username
    * проверяет username 
    ''')
    def test_login_control_username(self):
        assert self.welcome_page.get_username() == self.login_user.username

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct login-control block')
    @allure.title('Test logout redirect')
    @allure.description('''
    Проверка, что кнопка logout вызывает редирект на /login
    * нажимает logout
    * проверяет url 
    ''')
    def test_login_control_logout_web(self):
        self.welcome_page.click_logout()
        assert self.welcome_page.base_url + 'login' in self.driver.current_url

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct login-control block')
    @allure.title('Test logout changes active field')
    @allure.description('''
    Проверка, что кнопка logout вызывает вызывает изменнение поля active на 0
    * нажимает logout
    * проверяет, что поле active=0 
    ''')
    def test_login_control_logout_sql(self):
        self.welcome_page.click_logout()
        self.mysql_client.expire_all()
        assert self.login_user.active == 0


class TestUIWelcomeVkId(UIWelcomePageCase):

    @pytest.fixture(scope='function')
    def prepare(self):
        self.vk_user = self.builder.create_vk_user(self.login_user.username)
        self.driver.refresh()

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct vk_id block')
    @allure.title('Test correct vk_id is shown')
    @allure.description('''
    Проверка, что выводится верный vk_id
    * проверяет, что vk_id соответствует базе данных 
    ''')
    def test_vk_id_shown(self, prepare):
        assert self.welcome_page.get_vk_id() == self.vk_user.vk_id

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct vk_id block')
    @allure.title('Test vk_id is not shown')
    @allure.description('''
    Проверка, что vk_id не выводится, если отсутствует в БД
    * проверяет, что vk_id не выводится 
    ''')
    def test_vk_id_not_shown(self):
        with pytest.raises(TimeoutError):
            self.welcome_page.get_vk_id()

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct vk_id block')
    @allure.title('Test vk_id is not shown')
    @allure.description('''
    Проверка, что vk_id не выводится, если отсутствует в БД
    * проверяет, что vk_id не выводится 
    ''')
    def test_vk_id_not_shown_if_mock_down(self, prepare):
        self.app_mock_docker.mock_container.stop()
        self.driver.refresh()
        with pytest.raises(TimeoutError):
            self.welcome_page.get_vk_id()

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct vk_id block')
    @allure.title('Test vk_id is not shown if empty')
    @allure.description('''
    Проверка, что vk_id не выводится, если равен пустой строке
    * проверяет, что vk_id не выводится 
    ''')
    def test_vk_id_not_shown_if_empty(self, prepare):
        self.vk_user.vk_id = ''
        self.mysql_client.session.commit()
        self.driver.refresh()
        with pytest.raises(TimeoutError):
            self.welcome_page.get_vk_id()

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct vk_id block')
    @allure.title('Test long vk_id dont overlap navbar')
    @allure.description('''
    Проверка, что длинный vk_id не перекрывает кнопки навигации
    * добавляет в бд длинный vk_id 
    * проверяет, что на кнопку HOME возможно нажать
    ''')
    def test_vk_id_dont_overlap(self, prepare):
        self.vk_user.vk_id = 't' * 200
        self.mysql_client.session.commit()
        self.driver.set_window_size(1024, 900)
        self.driver.refresh()
        self.welcome_page.move_cursor_to_vk_id()
        self.welcome_page.click_navbar_list('Python')
        assert 'python' in self.driver.current_url


class TestUIWelcomeNavbar(UIWelcomePageCase):

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct navbar block')
    @allure.title('Test brand button redirect')
    @allure.description('''
    Проверка, редиректа на /welcome при нажатии на лого
    * запоминает текущий url
    * нажимает на лого
    * сверяет записанный url с новым
    ''')
    def test_brand_button(self):
        url = self.driver.current_url
        self.welcome_page.click_brand_button()
        assert url == self.driver.current_url

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct navbar block')
    @allure.title('Test HOME button redirect')
    @allure.description('''
    Проверка, редиректа на /welcome при нажатии на HOME
    * запоминает текущий url
    * нажимает на HOME
    * сверяет записанный url с новым
    ''')
    def test_home_button(self):
        url = self.driver.current_url
        self.welcome_page.click_home_button()
        assert url == self.driver.current_url

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct navbar block')
    @allure.title('Test navbar lists redirect')
    @allure.description('''
    Проверка, редиректа на верные страницы при нажатии на кнопки в навбаре
    * нажимает на кнопку в навбаре
    * проверяет соответствующее вхождение в url
    ''')
    @pytest.mark.parametrize('item', [
        'Python', 'Linux', 'Network'
    ])
    def test_navbar_list_buttons(self, item):
        self.welcome_page.click_navbar_list(item)
        assert item.lower() in self.driver.current_url

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct navbar block')
    @allure.title('Test navbar list elements redirect')
    @allure.description('''
    Проверка, редиректа на верные страницы при нажатии на кнопки в списках в навбаре
    * нажимает на кнопку в навбаре
    * проверяет соответствующее вхождение в url
    ''')
    @pytest.mark.parametrize('n_list, item, expected_url_entry', [
        ('python', 'history', 'History_of_Python'),
        ('python', 'Flask', 'flask'),
        ('linux', 'Centos7', 'centos'),
        ('network', 'News', 'news'),
        ('network', 'Download', 'download'),
        ('network', 'Examples', 'examples'),
    ])
    def test_navbar_list_buttons(self, n_list, item, expected_url_entry):
        self.welcome_page.click_navbar_list_element(n_list, item)
        self.switch_tab()
        assert expected_url_entry in self.driver.current_url


class TestUIWelcomeBlock(UIWelcomePageCase):

    @pytest.fixture(scope='function')
    def prepare(self):
        self.login_user.access = 0
        self.mysql_client.session.commit()
        self.driver.refresh()

    @allure.epic('Myapp UI tests')
    @allure.feature('Welcome page tests')
    @allure.story('Correct blocked user behaviour')
    @allure.title('Test logout when blocked')
    @allure.description('''
    Проверка редиректа при блокировке пользователя
    * проставляет юзеру access=0
    * обновляет страницу
    * проверяет соответствующее вхождение в url
    ''')
    def test_logout_when_blocked(self, prepare):
        assert self.welcome_page.base_url + 'login' in self.driver.current_url
