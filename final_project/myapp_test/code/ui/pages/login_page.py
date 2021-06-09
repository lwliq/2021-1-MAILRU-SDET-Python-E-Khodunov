
from ui.locators.login_page_locators import LoginPageLocators
from ui.pages.base import BasePage
from ui.pages.welcome_page import WelcomePage
from utils.decorators import wait


class AlertIsEmpty(Exception):
    pass


class LoginPage(BasePage):

    locators = LoginPageLocators
    location = 'login'

    def __init__(self, driver, app_url):
        super(self.__class__, self).__init__(driver, app_url)

        self.username_input = self.find(self.locators.USERNAME_INPUT)
        self.password_input = self.find(self.locators.PASSWORD_INPUT)
        self.submit_button = self.find(self.locators.LOGIN_BUTTON)
        self.registration_link = self.find(self.locators.REGISTRATION_LINK)

    def enter_username(self, username):
        self.send_keys(self.username_input, username, clear=True)

    def enter_password(self, password):
        self.send_keys(self.password_input, password, clear=True)

    def click_submit(self):
        self.click(self.submit_button)

    def get_validation_messages(self):
        validation_msgs = {
            'username': self.username_input.get_attribute('validationMessage'),
            'password': self.password_input.get_attribute('validationMessage')
        }
        return validation_msgs

    def get_alert_message(self):
        alert = self.find(self.locators.LOGIN_ALERT)

        def _check_element_has_text(element):
            if len(element.text) == 0:
                raise AlertIsEmpty(
                    'Could not get text from alert'
                )
            return element.text

        text = wait(
            method=_check_element_has_text,
            error=AlertIsEmpty,
            check=True,
            timeout=10,
            interval=0.1,
            element=alert
        )

        return text

    def get_alert_type(self):
        classes = self.find(self.locators.LOGIN_ALERT).get_attribute('class').split(' ')
        alert_type = [i for i in classes if 'uk-alert-' in i][0].split('-')[-1]
        return alert_type

    def go_to_registration_page(self):
        self.click(self.registration_link)

    def submit_and_go_to_welcome_page(self):
        self.click_submit()
        return WelcomePage(self.driver, self.base_url)



