from ui.locators.registration_page_locators import RegistrationPageLocators
from ui.pages.base import BasePage
from ui.pages.welcome_page import WelcomePage
from utils.decorators import wait


class AlertIsEmpty(Exception):
    pass


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators
    location = 'reg'

    def __init__(self, driver, app_url):
        super(self.__class__, self).__init__(driver, app_url)

        self.username_input = self.find(self.locators.USERNAME_INPUT)
        self.email_input = self.find(self.locators.EMAIL_INPUT)
        self.password_input = self.find(self.locators.PASSWORD_INPUT)
        self.confirm_input = self.find(self.locators.PASSWORD_CONFIRM_INPUT)
        self.term_checkbox = self.find(self.locators.TERM_CHECKBOX)
        self.submit_button = self.find(self.locators.REGISTRATION_BUTTON)
        self.login_link = self.find(self.locators.LOGIN_LINK)

    def enter_all_creds_dict(self, creds: dict, term=True):
        self.enter_username(creds['username'])
        self.enter_email(creds['email'])
        self.enter_both_passwords(creds['password'])
        self.enter_username(creds['username'])

        if term:
            self.click_term_checkbox()

    def enter_username(self, username: str):
        self.send_keys(self.username_input, username, clear=True)

    def enter_email(self, email: str):
        self.send_keys(self.email_input, email, clear=True)

    def enter_password(self, password: str):
        self.send_keys(self.password_input, password, clear=True)

    def enter_confirm(self, password: str):
        self.send_keys(self.confirm_input, password, clear=True)

    def enter_both_passwords(self, password: str):
        self.enter_password(password)
        self.enter_confirm(password)

    def click_term_checkbox(self):
        self.click(self.term_checkbox)

    def click_submit(self):
        self.click(self.submit_button)

    def get_validation_messages(self):
        validation_msgs = {
            'username': self.username_input.get_attribute('validationMessage'),
            'email': self.email_input.get_attribute('validationMessage'),
            'password': self.password_input.get_attribute('validationMessage'),
            'confirm': self.confirm_input.get_attribute('validationMessage'),
            'term': self.term_checkbox.get_attribute('validationMessage')
        }
        return validation_msgs

    def get_alert_message(self):
        alert = self.find(self.locators.REGISTRATION_ALERT)

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
        classes = self.find(self.locators.REGISTRATION_ALERT).get_attribute('class').split(' ')
        alert_type = [i for i in classes if 'uk-alert-' in i][0].split('-')[-1]
        return alert_type

    def go_to_login_page(self):
        self.click(self.login_link)

    def submit_and_go_to_welcome_page(self):
        self.click_submit()
        return WelcomePage(self.driver, self.base_url)

