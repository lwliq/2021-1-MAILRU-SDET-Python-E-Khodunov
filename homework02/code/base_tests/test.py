import os
import allure
import pytest

from base_tests.base import BaseCase
from datetime import datetime


@pytest.mark.UI
class TestInvalidLogin(BaseCase):

    authorize = False

    @allure.epic('Target UI tests')
    @allure.feature('Negative login tests')
    @allure.story('Invalid username test')
    def test_login_invalid_username(self):
        login_page = self.login_page

        login_page.login(
            email='test'
        )

        assert login_page.is_element_present(
            locator=login_page.locators.TARGET_ERROR_NOTIFICATION,
        )

    @allure.epic('Target UI tests')
    @allure.feature('Negative login tests')
    @allure.story('Wrong credentials test')
    def test_login_wrong_credentials(self):
        login_page = self.login_page

        login_page.login(
            email='test@test.com'
        )

        notification = login_page.find(login_page.locators.MYCOM_ERROR_NOTIFICATION)

        assert login_page.is_element_present(
            locator=login_page.locators.MYCOM_ERROR_NOTIFICATION,
        )


@pytest.mark.UI
class TestCampaigns(BaseCase):
    def file_path(self, *path):
        return os.path.join(self.repo_root, "base_tests", "files", *path)

    @allure.epic('Target UI tests')
    @allure.feature('Campaigns tests')
    @allure.story('Create new campaign test')
    def test_new_campaign(self):
        campaign_page = self.dashboard_page.go_to_new_campaign()

        campaign_name = "test_new_campaign_" + str(datetime.now())
        campaign_page.create_new_campaign(
            campaign_name=campaign_name,
            image_file_path=self.file_path("banner_test_image.jpeg")
        )

        assert self.dashboard_page.is_element_present_template(
            locator=self.dashboard_page.locators.CAMPAIGN_CELL_TEMPLATE,
            value=campaign_name,
        )

        self.dashboard_page.delete_campaign(campaign_name)


@pytest.mark.UI
class TestSegments(BaseCase):

    @allure.epic('Target UI tests')
    @allure.feature('Segments tests')
    @allure.story('Create new segment test')
    def test_new_segment(self):
        segments_page = self.dashboard_page.go_to_segments()

        segment_name = "test_new_segment_" + str(datetime.now())
        segments_page.create_new_segment(segment_name)

        assert segments_page.is_element_present_template(
            locator=segments_page.locators.Table.TITLE_CELL_TEMPLATE,
            value=segment_name,
        )

        segments_page.delete_segment(segment_name)

    @allure.epic('Target UI tests')
    @allure.feature('Segments tests')
    @allure.story('Delete segment test')
    def test_delete_segment(self):
        segments_page = self.dashboard_page.go_to_segments()

        segment_name = "test_delete_segment_" + str(datetime.now())
        segments_page.create_new_segment(segment_name)
        segments_page.delete_segment(segment_name)

        assert not segments_page.is_element_present_template(
            locator=segments_page.locators.Table.TITLE_CELL_TEMPLATE,
            value=segment_name,
            timeout=2
        )
