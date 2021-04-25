from datetime import datetime

import allure
import pytest

from base import ApiBase


@pytest.mark.API
class TestCampaigns(ApiBase):

    @pytest.fixture(scope='function')
    def campaign(self, request, repo_root):
        campaign_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_') + str(datetime.now())

        campaign_id, banner_ids = self.api_client.create_campaign(campaign_name, 'upload_image.jpg',
                                                                  self.file_path('upload_image.jpg'))

        yield campaign_id

        self.api_client.delete_campaign(campaign_id, banner_ids)

    @allure.epic('Target API tests')
    @allure.story('Campaigns tests')
    @allure.feature('Create new campaign test')
    def test_new_campaign(self, campaign):
        campaign_id = campaign

        assert self.api_client.check_if_campaign_has_status(campaign_id, 'active')


@pytest.mark.API
class TestSegments(ApiBase):
    @allure.epic('Target API tests')
    @allure.story('Segments tests')
    @allure.feature('Create new segment test')
    def test_new_segment(self):
        segment_name = 'test_new_segment_' + str(datetime.now())
        logic_type = 'and'

        segment_id = self.api_client.create_segment(segment_name, logic_type)

        assert self.api_client.check_if_segment_exists(segment_id)

        self.api_client.delete_segment(segment_id)

    @allure.epic('Target API tests')
    @allure.story('Segments tests')
    @allure.feature('Delete segment test')
    def test_delete_segment(self):
        segment_name = 'test_delete_segment_' + str(datetime.now())
        logic_type = 'or'

        segment_id = self.api_client.create_segment(segment_name, logic_type)
        self.api_client.delete_segment(segment_id)

        assert not self.api_client.check_if_segment_exists(segment_id)
