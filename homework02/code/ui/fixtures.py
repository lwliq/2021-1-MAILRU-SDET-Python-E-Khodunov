import os
import shutil

import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, FirefoxProfile
from selenium.webdriver import FirefoxProfile
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.login_page import LoginPage


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture(scope='function')
def dashboard_page(driver, login_page: LoginPage):
    login_page.login()
    return DashboardPage(login_page.driver)


def get_driver(browser_name, download_dir):
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": download_dir})
        options.add_argument("--lang=ru-ru")

        manager = ChromeDriverManager(version='latest', log_level=0)
        browser = webdriver.Chrome(executable_path=manager.install(), options=options)
    elif browser_name == 'firefox':
        profile = FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)  # 2 - download do directory specified in download.dir
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", download_dir)
        # no download helper when downloading specified filetypes
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/png")

        options = FirefoxOptions()
        options.profile = profile

        manager = GeckoDriverManager(version='latest', log_level=0)
        browser = webdriver.Firefox(executable_path=manager.install(), options=options)
    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')

    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    browser_name = config['browser']

    browser = get_driver(browser_name, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir, config):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        if config['browser'] == 'chrome':
            browser_logfile = os.path.join(test_dir, 'browser.log')
            with open(browser_logfile, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

            with open(browser_logfile, 'r') as f:
                allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)
