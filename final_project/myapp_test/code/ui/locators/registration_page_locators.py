from selenium.webdriver.common.by import By


class RegistrationPageLocators:

    USERNAME_INPUT = (By.XPATH, '//form[@action="/reg"]//input[@name="username"]')
    EMAIL_INPUT = (By.XPATH, '//form[@action="/reg"]//input[@name="email"]')
    PASSWORD_INPUT = (By.XPATH, '//form[@action="/reg"]//input[@name="password"]')
    PASSWORD_CONFIRM_INPUT = (By.XPATH, '//form[@action="/reg"]//input[@name="confirm"]')
    TERM_CHECKBOX = (By.XPATH, '//form[@action="/reg"]//input[@name="term"]')
    REGISTRATION_BUTTON = (By.XPATH, '//form[@action="/reg"]//input[@name="submit"]')

    LOGIN_LINK = (By.XPATH, '//form[@action="/reg"]//a[@href="/login"]')
    REGISTRATION_ALERT = (By.XPATH, '//form[@action="/reg"]//div[@id="flash"]')
