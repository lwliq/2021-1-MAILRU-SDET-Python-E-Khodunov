import allure
from selenium.common.exceptions import NoSuchElementException

from ui.exceptions import ElementIsPresentException
from ui.locators.pages_locators import SegmentsPageLocators
from ui.pages.base_page import BasePage
from utils.decorators import wait


class SegmentsPage(BasePage):

    locators = SegmentsPageLocators
    url = "https://target.my.com/segments/segments_list"

    @allure.step("Creating new segment {segment_name}")
    def create_new_segment(self, segment_name):

        try:
            self.click(self.locators.NEW_SEGMENT_INSTRUCTIONS_LINK)
        except TimeoutError:
            self.click(self.locators.NEW_SEGMENT_BUTTON, timeout=3)

        self.click_template(self.locators.SEGMENTS_CATEGORY_TEMPLATE, "Приложения и игры в соцсетях")
        self.click_template(self.locators.SEGMENT_CHECKBOX_TEMPLATE, "Игравшие и платившие в платформе")
        self.click(self.locators.ADD_SEGMENT_BUTTON)
        self.send_keys(self.locators.SEGMENT_NAME_INPUT, segment_name, clear=True)

        self.click(self.locators.CREATE_SEGMENT_BUTTON)

    @allure.step("Deleting segment {segment_name}")
    def delete_segment(self, segment_name):
        def _check_if_segment_deleted(segment_name, inside_timeout):
            if self.is_element_present_template(
                self.locators.Table.TITLE_CELL_TEMPLATE,
                segment_name,
                timeout=inside_timeout
            ):
                raise ElementIsPresentException

            return True

        element = self.find_template(self.locators.Table.TITLE_CELL_TEMPLATE, segment_name)
        segment_id = element.get_attribute('data-test').split('-')[-1]

        self.click_template(self.locators.Table.REMOVE_BUTTON_TEMPLATE, segment_id)
        self.click(self.locators.CONFIRM_REMOVE_BUTTON)

        wait(
            method=_check_if_segment_deleted,
            error=ElementIsPresentException,
            check=True,
            timeout=5,
            interval=0.2,
            segment_name=segment_name,
            inside_timeout=1
        )
