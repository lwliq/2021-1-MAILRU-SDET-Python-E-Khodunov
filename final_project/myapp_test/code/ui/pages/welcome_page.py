from ui.locators.welcome_page_locators import WelcomePageLocators
from ui.pages.base import BasePage


class WrongNavbarListNameException(Exception):
    pass


class WelcomePage(BasePage):

    locators = WelcomePageLocators
    location = 'welcome/'

    def __init__(self, driver, app_url):
        super(self.__class__, self).__init__(driver, app_url)

    def get_username(self):
        return self.find(self.locators.LoginControls.LOGGED_AS_LABEL).text.replace('Logged as ', '')

    def get_vk_id(self):
        return self.find(self.locators.LoginControls.VK_ID_LABEL, 3).text.replace('VK ID: ', '')

    def click_navbar_list(self, value):
        self.click_locator_template(self.locators.Navbar.NAVBAR_LIST_TEMPLATE, value)

    def click_navbar_list_element(self, list_name, value):
        if list_name == 'python':
            navbar_list = self.find_template(self.locators.Navbar.NAVBAR_LIST_TEMPLATE, 'Python')
            navbar_elem = self.find_template(self.locators.Navbar.PYTHON_LIST_TEMPLATE, value)
        elif list_name == 'linux':
            navbar_list = self.find_template(self.locators.Navbar.NAVBAR_LIST_TEMPLATE, 'Linux')
            navbar_elem = self.find_template(self.locators.Navbar.LINUX_LIST_TEMPLATE, value)
        elif list_name == 'network':
            navbar_list = self.find_template(self.locators.Navbar.NAVBAR_LIST_TEMPLATE, 'Network')
            navbar_elem = self.find_template(self.locators.Navbar.NETWORK_LIST_TEMPLATE, value)
        else:
            raise WrongNavbarListNameException()

        self.action_chains.move_to_element(navbar_list).perform()
        self.click(navbar_elem)

    def click_brand_button(self):
        self.click_locator(self.locators.Navbar.BRAND_BUTTON)

    def click_home_button(self):
        self.click_locator(self.locators.Navbar.HOME_BUTTON)

    def move_cursor_to_vk_id(self):
        vk_id = self.find(self.locators.LoginControls.VK_ID_LABEL)
        self.action_chains.move_to_element(vk_id).perform()

    def get_alert_text(self):
        return self.find(self.locators.ALERT).text

    def click_logout(self):
        self.click_locator(self.locators.LoginControls.LOGOUT_BUTTON)

    def click_content_link(self, value):
        self.click_locator_template(self.locators.CONTENT_BUTTON_TEMPLATE, value)

    def get_python_quote_text(self):
        return self.find(self.locators.PYTHON_QUOTE).text
