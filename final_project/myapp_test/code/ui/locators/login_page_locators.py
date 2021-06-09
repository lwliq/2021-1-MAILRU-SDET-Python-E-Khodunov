from selenium.webdriver.common.by import By


class LoginPageLocators:
    USERNAME_INPUT = (By.XPATH, '//form[@action="/login"]//input[@name="username"]')
    PASSWORD_INPUT = (By.XPATH, '//form[@action="/login"]//input[@name="password"]')
    LOGIN_BUTTON = (By.XPATH, '//form[@action="/login"]//input[@name="submit"]')

    REGISTRATION_LINK = (By.XPATH, '//form[@action="/login"]//a[@href="/reg"]')
    LOGIN_ALERT = (By.XPATH, '//form[@action="/login"]//div[@id="flash"]')
