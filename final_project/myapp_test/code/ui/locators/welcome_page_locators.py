from selenium.webdriver.common.by import By


class WelcomePageLocators:

    class LoginControls:
        LOGIN_CONTROLS = (By.XPATH, '//div[@id="login-controls"]')
        LOGOUT_BUTTON = (By.XPATH, '//div[@id="login-controls"]//a[@href="/logout"]')
        LOGGED_AS_LABEL = (By.XPATH, '//div[@id="login-controls"]//li[contains(text(), "Logged as")]')
        VK_ID_LABEL = (By.XPATH, '//div[@id="login-controls"]//li[contains(text(), "VK ID")]')

    class Navbar:
        BRAND_BUTTON = (By.XPATH, '//header//a[contains(@class, "uk-navbar-brand")]')
        HOME_BUTTON = (By.XPATH, '//header//a[contains(text(), "HOME")]')

        NAVBAR_LIST_TEMPLATE = (By.XPATH, '//header//li[@class="uk-parent"]/a[contains(text(), "{}")]')
        PYTHON_LIST_TEMPLATE = (By.XPATH, NAVBAR_LIST_TEMPLATE[1].format('Python') + '/..//a[contains(text(), "{}")]')
        LINUX_LIST_TEMPLATE = (By.XPATH, NAVBAR_LIST_TEMPLATE[1].format('Linux') + '/..//a[contains(text(), "{}")]')
        NETWORK_LIST_TEMPLATE = (By.XPATH, NAVBAR_LIST_TEMPLATE[1].format('Network') + '/..//a[contains(text(), "{}")]')

    CONTENT_BUTTON_TEMPLATE = (By.XPATH, '//div[@id="content"]//div[contains(text(), "{}")]//../figure')
    PYTHON_QUOTE = (By.XPATH, '//footer//p[not(contains(text(), "ТЕХНОАТОМ"))]')

    ALERT = (By.XPATH, '//form[@action="/login"]//div[@id="flash"]')
