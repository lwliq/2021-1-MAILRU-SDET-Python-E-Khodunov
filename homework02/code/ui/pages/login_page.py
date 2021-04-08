import credentials
from ui.locators.pages_locators import LoginPageLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):

    locators = LoginPageLocators

    def login(self, email=credentials.EMAIL, password=credentials.PASSWORD):
        self.click(self.locators.LOGIN_BUTTON_LOCATOR)

        email_input = self.find(self.locators.EMAIL_INPUT_LOCATOR)
        email_input.send_keys(email)

        password_input = self.find(self.locators.PASSWORD_INPUT_LOCATOR)
        password_input.send_keys(password)

        self.click(self.locators.SUBMIT_BUTTON_LOCATOR)
