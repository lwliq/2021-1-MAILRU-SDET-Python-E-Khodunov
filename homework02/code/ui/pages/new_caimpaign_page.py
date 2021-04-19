import time

import allure

from ui.exceptions import UnsupportedRegionActionTypeException, UnsupportedBannerTypeException
from ui.pages.base_page import BasePage
from ui.locators.pages_locators import NewCampaignPageLocators


class NewCampaignPage(BasePage):
    url = "https://target.my.com/campaign/new"
    locators = NewCampaignPageLocators

    @allure.step("Setting sex to {sex_checkbox}")
    def set_sex(self, sex_checkbox='sex-male'):
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'sex')
        self.click_template(self.locators.Targeting.SEX_CHECKBOX_TEMPLATE, sex_checkbox)

    @allure.step("Setting age range to {age_range}")
    def set_age(self, age_range='?'):
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'age')
        self.click(self.locators.Targeting.AGE_SELECT_MENU)
        self.click_template(self.locators.Targeting.AGE_SELECT_ITEM_TEMPLATE, 'custom')
        self.send_keys(self.locators.Targeting.AGE_CUSTOM_TEXTAREA, age_range, clear=True)

    @allure.step("Performing region action {action_type} with region {region}")
    def region_action(self, region, action_type='add'):
        if action_type == 'add':
            self.send_keys(self.locators.Targeting.GEO_REGION_INPUT, region, clear=True)
            self.click_template(self.locators.Targeting.GEO_REGION_ADD_BUTTON_TEMPLATE, region)
        elif action_type == 'exclude':
            self.send_keys(self.locators.Targeting.GEO_REGION_INPUT, region, clear=True)
            self.click_template(
                self.locators.Targeting.GEO_REGION_EXCLUDE_BUTTON_TEMPLATE,
                region
            )
        elif action_type == 'remove':
            self.click_template(
                self.locators.Targeting.GEO_SELECTED_REGIONS_REMOVE_TEMPLATE,
                region
            )
        else:
            raise UnsupportedRegionActionTypeException

    @allure.step("Adding soc dem interest {group_item} from group {group_name}")
    def set_interests_soc_dem(self, group_name, group_item):
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'interests_soc_dem')
        self.click_template(
            self.locators.Targeting.INTERESTS_SOC_DEM_GROUP_COLLAPSE_TEMPLATE,
            group_name
        )
        self.click_template(
            self.locators.Targeting.INTERESTS_SOC_DEM_GROUP_ITEM_CHECKBOX_TEMPLATE,
            group_item
        )

    @allure.step("Adding interest {group_item} from group {group_name}")
    def set_interests(self, group_name, group_item):
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'interests')
        self.click_template(
            self.locators.Targeting.INTERESTS_GROUP_COLLAPSE_TEMPLATE,
            group_name
        )
        self.click_template(
            self.locators.Targeting.INTERESTS_GROUP_ITEM_CHECKBOX_TEMPLATE,
            group_item
        )

    @allure.step("Setting time preset to {time_preset}")
    def set_full_time(self, time_preset):
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'fulltime')
        self.click_template(
            self.locators.WhenTargeting.FULL_TIME_SETTING_PRESET_TEMPLATE,
            time_preset
        )

    @allure.step("Setting campaign date to from={date_from} to={date_to}")
    def set_date(self, date_from, date_to):
        self.click_template(self.locators.EXPANDABLE_MENU_TEMPLATE, 'date')
        self.send_keys_template(self.locators.WhenTargeting.DATE_INPUT_TEMPLATE, "date-from", date_from)
        self.send_keys_template(self.locators.WhenTargeting.DATE_INPUT_TEMPLATE, "date-to", date_to)

    @allure.step("Setting budget to daily={budget_daily} total={budget_total}")
    def set_budget(self, budget_daily, budget_total):
        self.send_keys_template(self.locators.BudgetTargeting.BUDGET_INPUT_TEMPLATE, "budget-per_day", budget_daily)
        self.send_keys_template(self.locators.BudgetTargeting.BUDGET_INPUT_TEMPLATE, "budget-total", budget_total)

    @allure.step("Creating banner {banner_name}")
    def create_banner(self, banner_type, banner_name, banner_title, banner_text, banner_info, image_file_path):
        if banner_type == 'Мультиформат':
            self.click_template(
                self.locators.BannerFormats.BANNER_FORMAT_TEMPLATE,
                banner_type
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
        else:
            raise UnsupportedBannerTypeException

        self.send_keys(self.locators.BannerEditor.BANNER_NAME_INPUT, banner_name)
        self.click(self.locators.BannerEditor.BANNER_SUBMIT_BUTTON)

    @allure.step("Creating campaign {campaign_name}")
    def create_new_campaign(self, campaign_name, campaign_info):

        self.click_template(self.locators.OBJECTIVE_BUTTON_TEMPLATE, campaign_info['campaign_type'])

        self.send_keys(self.locators.URL_INPUT, campaign_info['campaign_url'])

        self.send_keys(self.locators.CAMPAIGN_NAME_INPUT, campaign_name, clear=True)

        self.set_sex(sex_checkbox=campaign_info['sex_checkbox'])

        self.set_age(age_range=campaign_info['age_range'])

        self.region_action(campaign_info['region_to_add'], 'add')
        self.region_action(campaign_info['region_to_exclude'], 'exclude')
        self.region_action(campaign_info['region_to_remove'], 'remove')

        self.set_interests_soc_dem(campaign_info['interest_soc_dem_group'], campaign_info['interest_soc_dem_item'])

        self.set_interests(campaign_info['interest_group'], campaign_info['interest_item'])

        self.set_full_time(campaign_info['full_time_preset'])

        self.set_date(campaign_info['date_from'], campaign_info['date_to'])

        self.set_budget(campaign_info['budget_daily'], campaign_info['budget_total'])

        self.create_banner(
            banner_name=campaign_name,
            banner_type=campaign_info['banner_type'],
            banner_title=campaign_info['banner_title'],
            banner_text=campaign_info['banner_text'],
            banner_info=campaign_info['banner_info'],
            image_file_path=campaign_info['image_file_path']
        )

        self.click(self.locators.CAMPAIGN_SUBMIT_BUTTON)
