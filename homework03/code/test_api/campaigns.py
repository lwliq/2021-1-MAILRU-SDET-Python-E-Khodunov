import os
from datetime import datetime

import allure
import pytest
from test_api.base import ApiBase


class CampaingsApi(ApiBase):
    def file_path(self, *path):
        return os.path.join(self.repo_root, "test_api", "files", *path)

    @pytest.fixture(scope='function')
    def campaign(self, request):
        campaign_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_') + str(datetime.now())

        campaign_id, banner_ids = self.create_campaign(campaign_name)

        yield campaign_id

        self.delete_campaign(campaign_id, banner_ids)

    @allure.step('Creating campaign {campaign_name}')
    def create_campaign(self, campaign_name):
        url_id = self.api_client.get_url_id('https://google.com/')
        image_600x600_id = self.api_client.post_image_upload('upload_image.jpg', self.file_path('upload_image.jpg'), 600, 600)
        image_1080x607_id = self.api_client.post_image_upload('upload_image.jpg', self.file_path('upload_image.jpg'),
                                                              1080, 607)
        icon_256x256_id = self.api_client.post_image_upload('upload_image.jpg', self.file_path('upload_image.jpg'), 256, 256)

        banner_info = {
            'content': {
                'image_600x600': {'id': image_600x600_id},
                'image_1080x607': {'id': image_1080x607_id},
                'icon_256x256': {'id': icon_256x256_id}
            },
            'name': campaign_name,
            'textblocks': {
                'cta_sites_full': {'text': 'visitSite'},
                'text_90': {'text': 'Тест'},
                'title_25': {'text': 'Тест'}
            },
            'urls': {
                'primary': {'id': url_id}
            }
        }

        targetings_info = {
            'age': {
                'age_list': [i for i in range(60) if i > 12],
                'expand': True
            },
            'fulltime': {
                'flags': ["use_holidays_moving", "cross_timezone"],
                'mon': [i for i in range(24)]
            },
            'geo': {'regions': [188]},
            'interests': [],
            'interests_soc_dem': [],
            'mobile_operators': [],
            'mobile_types': ["tablets", "smartphones"],
            'mobile_vendors': [],
            'pads': [102634, 102643],
            'segments': [],
            'sex': ["male", "female"],
            'split_audience': [i+1 for i in range(10)]
        }

        payload = {
            'autobidding_mode': 'second_price_mean',
            'banners': [banner_info],
            'enable_offline_goals': False,
            'enable_utm': True,
            'max_price': '0',
            'mixing': 'fastest',
            'name': campaign_name,
            'objective': 'traffic',
            'package_id': 811,
            'price': '10.0',
            'targetings': targetings_info
        }

        campaign_id, banner_ids = self.api_client.post_campaign_create(payload)

        return campaign_id, banner_ids

    @allure.step('Deleting campaign id={campaign_id}')
    def delete_campaign(self, campaign_id, banner_ids):
        for b_id in banner_ids:
            self.api_client.post_banner_delete(b_id)

        self.api_client.post_campaign_delete(campaign_id)

    def check_if_campaign_has_status(self, campaign_id, status):
        return campaign_id in self.api_client.get_campaigns_ids_list(status)
