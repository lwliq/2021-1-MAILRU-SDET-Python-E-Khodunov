import pytest
from selenium import webdriver


URL = "https://target.my.com/"


@pytest.fixture(scope='session')
def driver():
    browser = webdriver.Chrome()
    browser.set_window_size(1400, 1000)
    browser.get(URL)
    yield browser
    browser.close()
