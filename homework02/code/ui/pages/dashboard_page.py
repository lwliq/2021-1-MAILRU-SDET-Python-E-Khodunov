import allure

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import DashboardPageLocators
from ui.pages.new_caimpaign_page import NewCampaignPage
from ui.pages.segments_page import SegmentsPage
from utils.decorators import wait


class DashboardPage(BasePage):

    url = "https://target.my.com/dashboard"
    locators = DashboardPageLocators()

    def go_to_new_campaign(self):
        try:
            self.click(self.locators.NEW_CAMPAIGN_BUTTON, timeout=5)
        except TimeoutError:
            self.click(self.locators.NEW_CAMPAIGN_INSTRUCTIONS_LINK)

        return NewCampaignPage(driver=self.driver)

    def go_to_segments(self):
        self.click(self.locators.SEGMENTS_RIBBON_BUTTON)
        return SegmentsPage(driver=self.driver)

    def get_table_item_id(self, item_name, item_type="banner"):
        if item_type == "campaign":
            item = self.find_template(self.locators.CAMPAIGN_CELL_TEMPLATE, item_name)
        else:
            item = self.find_template(self.locators.BANNER_CELL_TEMPLATE, item_name)

        return item.get_attribute('data-test').split('-')[-1]

    def is_table_item_deleted(self, item_name, item_type="banner"):
        item_id = self.get_table_item_id(item_name, item_type)
        cell = self.find_template(self.locators.Table.STATUS_CELL_TEMPLATE, item_id)
        assert cell.get_attribute("innerHTML") in ("Кампания удалена", "Удалено")
        return True

    @allure.step("Deleting campaign {campaign_name}")
    def delete_campaign(self, campaign_name):

        self.click_template(self.locators.CAMPAIGN_COLLAPSE_BUTTON_TEMPLATE, campaign_name)

        self.click_template(self.locators.BANNER_SELECT_CHECKBOX_TEMPLATE, campaign_name)
        self.click(self.locators.TABLE_CONTROLS_SELECT)
        self.click_template(self.locators.SELECT_LIST_ITEM_TEMPLATE, "Удалить")
        self.click_template(self.locators.BANNER_SELECT_CHECKBOX_TEMPLATE, campaign_name)

        wait(
            method=self.is_table_item_deleted,
            error=AssertionError,
            check=True,
            timeout=5,
            interval=0.1,
            item_name=campaign_name,
            item_type="banner"
        )

        self.click_template(self.locators.CAMPAIGN_SELECT_CHECKBOX_TEMPLATE, campaign_name)
        self.click(self.locators.TABLE_CONTROLS_SELECT)
        self.click_template(self.locators.SELECT_LIST_ITEM_TEMPLATE, "Удалить")
        self.click_template(self.locators.CAMPAIGN_SELECT_CHECKBOX_TEMPLATE, campaign_name)

        self.click_template(self.locators.CAMPAIGN_COLLAPSE_BUTTON_TEMPLATE, campaign_name)

        wait(
            method=self.is_table_item_deleted,
            error=AssertionError,
            check=False,
            timeout=5,
            interval=0.1,
            item_name=campaign_name,
            item_type="campaign"
        )
