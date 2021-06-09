import os
import shutil

import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from ui.pages.login_page import LoginPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.welcome_page import WelcomePage


class NoSelenoidURLException(Exception):
    pass


@pytest.fixture(scope='function')
def login_page(driver, app_url):
    driver.get(app_url + 'login')
    return LoginPage(driver, app_url)


@pytest.fixture(scope='function')
def registration_page(driver, app_url):
    driver.get(app_url + 'reg')
    return RegistrationPage(driver, app_url)


@pytest.fixture(scope='function')
def welcome_page(driver, app_url):
    driver.get(app_url + 'welcome/')
    return WelcomePage(driver, app_url)


def get_driver(config):
    selenoid = config['selenoid']
    vnc = config['vnc']

    options = ChromeOptions()

    if selenoid is not None:
        caps = {'browserName': 'chrome',
                'version': '89.0',
                'sessionTimeout': '2m'}

        if vnc:
            caps['version'] += '_vnc'
            caps['enableVNC'] = True

        browser = webdriver.Remote(selenoid + '/wd/hub', options=options, desired_capabilities=caps)

    else:
        raise NoSelenoidURLException()

    return browser


@pytest.fixture(scope='function')
def driver(config, app_url, test_dir, request):
    browser = get_driver(config)
    browser.get(app_url)
    browser.maximize_window()
    failed_tests_count = request.session.testsfailed

    yield browser

    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        browser.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in browser.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

    browser.quit()



