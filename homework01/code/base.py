import pytest
from ui.locators import login_locators
from ui.locators import basic_locators
import credentials
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

CLICK_RETRY = 4


class BaseCase:

    driver = None
    credentials = {
            "email": credentials.EMAIL,
            "password": credentials.PASSWORD
        }

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):

        self.driver = driver

    def wait(self, timeout=None):

        if timeout is None:
            timeout = 5

        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):

        try:
            return self.wait(timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise

    def click(self, locator, timeout=None):

        for i in range(CLICK_RETRY):
            try:
                element = self.wait(timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                return
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise

    def input_text(self, text, locator, timeout=None):

        element = self.find(locator, timeout)
        element.clear()
        element.send_keys(text)

    def spinner_wait(self, timeout=None):

        try:
            self.wait(timeout).until(
                EC.presence_of_element_located(basic_locators.LOAD_SPINNER_LOCATOR)
            )

            self.wait(timeout).until_not(
                EC.presence_of_element_located(basic_locators.LOAD_SPINNER_LOCATOR)
            )
        except TimeoutException:
            pass

    def my_login(self):
        self.spinner_wait(timeout=1)
        self.click(login_locators.LOGIN_BUTTON_LOCATOR)

        self.input_text(
            text=self.credentials['email'],
            locator=login_locators.EMAIL_INPUT_LOCATOR
        )

        self.input_text(
            text=self.credentials['password'],
            locator=login_locators.PASSWORD_INPUT_LOCATOR
        )

        self.click(login_locators.SUBMIT_BUTTON_LOCATOR)
        self.spinner_wait(timeout=1)

    @pytest.fixture(scope='function')
    def login(self):
        self.my_login()

    @pytest.fixture(scope='function')
    def logout(self):

        yield

        self.click(basic_locators.RIGHT_PROFILE_BUTTON_LOCATOR)
        sleep(0.5)
        self.click(
            locator=basic_locators.LOGOUT_BUTTON,
            timeout=2
        )
