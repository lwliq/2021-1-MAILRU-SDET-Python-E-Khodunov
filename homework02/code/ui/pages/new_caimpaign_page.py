import time

import allure

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import NewCampaignPageLocators


class NewCampaignPage(BasePage):
    url = "https://target.my.com/campaign/new"
    locators = NewCampaignPageLocators

    @allure.step("Creating campaign {campaign_name}")
    def create_new_campaign(self, campaign_name,  image_file_path):

        self.click_template(self.locators.OBJECTIVE_BUTTON_TEMPLATE, 'traffic')

        self.send_keys(self.locators.URL_INPUT, 'http://google.com/')

        self.send_keys(self.locators.CAMPAIGN_NAME_INPUT, campaign_name, clear=True)

        sex_checkbox = 'sex-male'
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'sex')
        self.click_template(self.locators.Targeting.SEX_CHECKBOX_TEMPLATE, sex_checkbox)

        age_range = '25-60'
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'age')
        self.click(self.locators.Targeting.AGE_SELECT_MENU)
        self.click_template(self.locators.Targeting.AGE_SELECT_ITEM_TEMPLATE, 'custom')
        self.send_keys(self.locators.Targeting.AGE_CUSTOM_TEXTAREA, age_range, clear=True)

        region_to_add = 'Москва'
        region_to_exclude = 'Воронеж'
        region_to_remove = 'Россия'
        self.send_keys(self.locators.Targeting.GEO_REGION_INPUT, region_to_add)
        self.click_template(self.locators.Targeting.GEO_REGION_ADD_BUTTON_TEMPLATE, region_to_add)
        self.send_keys(self.locators.Targeting.GEO_REGION_INPUT, region_to_exclude, clear=True)
        self.click_template(
            self.locators.Targeting.GEO_REGION_EXCLUDE_BUTTON_TEMPLATE,
            region_to_exclude
        )
        self.click_template(
            self.locators.Targeting.GEO_SELECTED_REGIONS_REMOVE_TEMPLATE,
            region_to_remove
        )

        interest_group = "Группы телесмотрения"
        interest_item = "Смотрят ТВ cредне"
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'interests_soc_dem')
        self.click_template(
            self.locators.Targeting.INTERESTS_SOC_DEM_GROUP_COLLAPSE_TEMPLATE,
            interest_group
        )
        self.click_template(
            self.locators.Targeting.INTERESTS_SOC_DEM_GROUP_ITEM_CHECKBOX_TEMPLATE,
            interest_item
        )

        interest_group = "Авто"
        interest_item = "Авто внедорожники"
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'interests')
        self.click_template(
            self.locators.Targeting.INTERESTS_GROUP_COLLAPSE_TEMPLATE,
            interest_group
        )
        self.click_template(
            self.locators.Targeting.INTERESTS_GROUP_ITEM_CHECKBOX_TEMPLATE,
            interest_item
        )

        full_time_preset = "workTime"
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'fulltime')
        self.click_template(
            self.locators.WhenTargeting.FULL_TIME_SETTING_PRESET_TEMPLATE,
            full_time_preset
        )

        date_from = "11.12.2020"
        date_to = "11.12.2022"
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'date')
        self.send_keys_template(self.locators.WhenTargeting.DATE_INPUT_TEMPLATE, "date-from", date_from)
        self.send_keys_template(self.locators.WhenTargeting.DATE_INPUT_TEMPLATE, "date-to", date_to)

        budget_daily = "1000"
        budget_total = "1000000"
        self.send_keys_template(self.locators.BudgetTargeting.BUDGET_INPUT_TEMPLATE, "budget-per_day", budget_daily)
        self.send_keys_template(self.locators.BudgetTargeting.BUDGET_INPUT_TEMPLATE, "budget-total", budget_total)

        self.click_template(
            self.locators.BannerFormats.BANNER_FORMAT_TEMPLATE,
            "Мультиформат"
        )

        self.send_keys_template(
            self.locators.BannerEditor.BANNER_IMAGE_INPUT_TEMPLATE,
            "image_1080x607",
            image_file_path,
            file=True
        )
        self.click(self.locators.BannerEditor.IMAGE_CROPPER_SUBMIT_BUTTON)
        self.send_keys_template(
            self.locators.BannerEditor.BANNER_IMAGE_INPUT_TEMPLATE,
            "icon_256x256",
            image_file_path,
            file=True
        )
        self.click(self.locators.BannerEditor.IMAGE_CROPPER_SUBMIT_BUTTON)
        self.send_keys_template(
            self.locators.BannerEditor.BANNER_IMAGE_INPUT_TEMPLATE,
            "image_600x600",
            image_file_path,
            file=True
        )
        self.click(self.locators.BannerEditor.IMAGE_CROPPER_SUBMIT_BUTTON)

        banner_title = "Тест"
        banner_text = "Тест"
        banner_info = "ОГРН 12233445555556"
        self.send_keys(self.locators.BannerEditor.BANNER_TITLE_INPUT, banner_title)
        self.send_keys_template(
            self.locators.BannerEditor.BANNER_TEXT_INPUT_TEMPLATE,
            'text',
            banner_text
        )
        self.send_keys_template(
            self.locators.BannerEditor.BANNER_TEXT_INPUT_TEMPLATE,
            'about_company',
            banner_info
        )
        self.send_keys(self.locators.BannerEditor.BANNER_NAME_INPUT, campaign_name)
        self.click(self.locators.BannerEditor.BANNER_SUBMIT_BUTTON)

        self.click(self.locators.CAMPAIGN_SUBMIT_BUTTON)
