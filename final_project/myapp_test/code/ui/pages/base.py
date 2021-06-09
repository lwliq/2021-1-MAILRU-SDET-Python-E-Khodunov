import logging
import os

import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from _pytest.fixtures import FixtureRequest
from ui.exceptions import PageNotLoadedException, ElementIsNotInteractableException

from utils.decorators import wait

INPUT_RETRY = 3
BASE_TIMEOUT = 10
CHECK_PRESENCE_RETRY = 3


logger = logging.getLogger('test')


class BasePage(object):
    location = ''

    def __init__(self, driver, app_url):
        self.driver: WebDriver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')
        self.base_url = app_url
        self.url = self.base_url + self.location
        assert self.is_opened()

    def is_opened(self):
        def _check_url():
            if self.driver.current_url != self.url:
                raise PageNotLoadedException(
                    f'{self.url} did not opened in {BASE_TIMEOUT} for {self.__class__.__name__}.\n'
                    f'Current url: {self.driver.current_url}.')
            return True

        return wait(
            method=_check_url,
            error=PageNotLoadedException,
            check=True,
            timeout=BASE_TIMEOUT,
            interval=0.1
        )

    @allure.step("Trying to find element {locator}")
    def find(self, locator, timeout=BASE_TIMEOUT) -> WebElement:
        logger.info(f'Trying to find element {locator}')
        element = wait(
            method=self.driver.find_element,
            error=NoSuchElementException,
            check=False,
            timeout=timeout,
            interval=0.1,
            by=locator[0],
            value=locator[1]
        )
        self.scroll_to(element)
        return element

    def find_template(self, locator, value, timeout=BASE_TIMEOUT):
        return self.find(
            locator=(
                locator[0],
                locator[1].format(value)
            ),
            timeout=timeout
        )

    def is_element_present(self, locator, timeout=BASE_TIMEOUT):
        try:
            self.find(locator, timeout)
        except TimeoutError:
            return False

        return True

    def is_element_present_template(self, locator, value, timeout=BASE_TIMEOUT):
        return self.is_element_present(
            locator=(
                locator[0],
                locator[1].format(value)
            ),
            timeout=timeout
        )

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def _check_element_is_interactable(self, elem: WebElement):
        if (not elem.is_displayed()) or (not elem.is_enabled()):
            raise ElementIsNotInteractableException(
                f'Element {elem.tag_name} on page {self.driver.current_url} is not interactable.'
            )
        return True

    @allure.step('Clicking {locator}')
    def click_locator(self, locator, timeout=BASE_TIMEOUT):
        element = self.find(locator, timeout)
        self.click(element, timeout)

    def click_locator_template(self, locator, value, timeout=BASE_TIMEOUT):
        self.click_locator(
            locator=(
                    locator[0],
                    locator[1].format(value)
            ),
            timeout=timeout
        )


    def click(self, element, timeout=BASE_TIMEOUT):
        for i in range(INPUT_RETRY):
            logger.info(f'Clicking on {element.tag_name}. Try {i + 1} of {INPUT_RETRY}...')
            try:
                wait(
                    method=self._check_element_is_interactable,
                    error=ElementIsNotInteractableException,
                    check=True,
                    timeout=timeout,
                    interval=0.2,
                    elem=element
                )

                element.click()
                return
            except ElementClickInterceptedException:
                if i == INPUT_RETRY - 1:
                    raise
            except StaleElementReferenceException:
                if i == INPUT_RETRY - 1:
                    raise

    def send_keys_locator(self, locator, keys, file=False, clear=False, timeout=BASE_TIMEOUT):
        element = self.find(locator, timeout)
        self.send_keys(element, keys, file, clear, timeout)

    def send_keys_locator_template(self, locator, value, keys, file=False, clear=False, timeout=BASE_TIMEOUT):
        self.send_keys_locator(
            locator=(
                locator[0],
                locator[1].format(value)
            ),
            file=file,
            clear=clear,
            timeout=timeout,
            keys=keys
        )

    @allure.step('Sending keys {keys} to {element}')
    def send_keys(self, element, keys, file=False, clear=False, timeout=BASE_TIMEOUT):
        for i in range(INPUT_RETRY):
            logger.info(f'Sending keys {keys} to {element.tag_name}. Try {i + 1} of {INPUT_RETRY}...')
            try:
                if not file:
                    wait(
                        method=self._check_element_is_interactable,
                        error=ElementIsNotInteractableException,
                        check=True,
                        timeout=timeout,
                        interval=0.2,
                        elem=element
                    )

                if clear:
                    element.clear()

                element.send_keys(keys)
                return
            except ElementIsNotInteractableException:
                if i == INPUT_RETRY - 1:
                    raise
            except StaleElementReferenceException:
                if i == INPUT_RETRY - 1:
                    raise
