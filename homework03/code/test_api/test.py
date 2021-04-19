from datetime import datetime

import allure
import pytest

from test_api.campaigns import CampaingsApi
from test_api.segments import SegmentsApi


@pytest.mark.API
class TestCampaigns(CampaingsApi):
    @allure.epic('Target API tests')
    @allure.story('Campaigns tests')
    @allure.feature('Create new campaign test')
    def test_new_campaign(self, campaign):
        campaign_id = campaign

        assert self.check_if_campaign_has_status(campaign_id, 'active')


@pytest.mark.API
class TestSegments(SegmentsApi):
    @allure.epic('Target API tests')
    @allure.story('Segments tests')
    @allure.feature('Create new segment test')
    def test_new_segment(self):
        segment_name = 'test_new_segment_' + str(datetime.now())
        logic_type = 'and'

        segment_id = self.create_segment(segment_name, logic_type)

        assert self.check_if_segment_exists(segment_id)

        self.api_client.delete_segment(segment_id)

    @allure.epic('Target API tests')
    @allure.story('Segments tests')
    @allure.feature('Delete segment test')
    def test_delete_segment(self):
        segment_name = 'test_delete_segment_' + str(datetime.now())
        logic_type = 'or'

        segment_id = self.create_segment(segment_name, logic_type)
        self.api_client.delete_segment(segment_id)

        assert not self.check_if_segment_exists(segment_id)
