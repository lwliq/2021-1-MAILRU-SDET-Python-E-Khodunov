import random
import string

import allure
import requests
from requests.cookies import cookiejar_from_dict

from urllib.parse import urljoin

from requests_toolbelt import MultipartEncoder


class ResponseStatusCodeException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class SegmentCreationFailedException(Exception):
    pass


class CampaignCreationFailedException(Exception):
    pass


class ImageUploadFailedException(Exception):
    pass


class WrongLogicTypeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url, login_url):

        self.base_url = base_url
        self.login_url = login_url
        self.session = requests.Session()
        self.csrf_token = None

    def _request(self, method, location, expected_status=200, jsonify=True, **kwargs):
        url = urljoin(self.base_url, location)

        response = self.session.request(method, url, **kwargs)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        if jsonify:
            return response.json()
        return response

    def post_login(self, user, password):
        data = {
            'email': user,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Referer': self.base_url
        }

        # Collecting authorization cookies
        response = self.session.request('POST', self.login_url, data=data, headers=headers)

        try:
            response.headers['Set-Cookie'].split(';')
        except Exception as e:
            raise InvalidLoginException(e)

        # Collecting csrftoken cookie
        self._request('GET', '/csrf', jsonify=False)
        self.csrf_token = self.session.cookies['csrftoken']

    def post_image_upload(self, file_name, file_path, width, height):

        resolution = '{' + f'"width":{width},"height":{height}' + '}'
        with open(file_path, 'rb') as file:
            fields = {
                'file': (file_name, file, 'image/jpeg'),
                'data': resolution
            }

            boundary = '----WebKitFormBoundary' \
                       + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            data = MultipartEncoder(fields=fields, boundary=boundary)

            headers = {
                'X-CSRFToken': self.csrf_token,
                'Content-Type': data.content_type,
            }

            response = self._request('POST', 'api/v2/content/static.json', data=data, headers=headers)

            if 'id' not in response.keys():
                raise ImageUploadFailedException

            return response['id']

    def get_url_id(self, url):
        params = {
            'url': url
        }

        response = self._request('GET', 'api/v1/urls/', params=params)

        return response['id']

    @property
    def json_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.csrf_token
        }

    def post_campaign_create(self, payload):
        headers = self.json_headers
        headers['X-Campaign-Create-Action'] = 'new'

        response = self._request('POST', 'api/v2/campaigns.json', headers=headers, json=payload)

        if 'id' not in response.keys():
            raise CampaignCreationFailedException

        return response['id'], [i['id'] for i in response['banners']]

    def post_banner_delete(self, banner_id):
        headers = self.json_headers

        payload = {
            'status': 'deleted'
        }

        self._request('POST', f'api/v2/banners/{banner_id}.json', expected_status=204, jsonify=False,
                      headers=headers, json=payload)

    def post_campaign_delete(self, campaign_id):
        headers = self.json_headers

        payload = {
            'status': 'deleted'
        }

        self._request('POST', f'api/v2/campaigns/{campaign_id}.json', expected_status=204, jsonify=False,
                      headers=headers, json=payload)

    def get_campaign(self, campaign_id):
        return self._request('GET', f'campaign/{campaign_id}', expected_status=200, jsonify=False)

    def post_segment_create(self, payload):
        headers = self.json_headers

        response = self._request('POST', 'api/v2/remarketing/segments.json', headers=headers, json=payload)

        if 'id' not in response.keys():
            raise SegmentCreationFailedException

        return response['id']

    @allure.step('Deleting segment id={segment_id}')
    def delete_segment(self, segment_id):
        headers = {
            'X-CSRFToken': self.csrf_token
        }

        self._request('DELETE', f'api/v2/remarketing/segments/{segment_id}.json', expected_status=204,
                      jsonify=False, headers=headers)

    def get_segments_ids_list(self):
        params = {
            'fields': ['id'],
            'limit': 500,
        }

        headers = {
            'X-CSRFToken': self.csrf_token,
        }

        ids = self._request('GET', f'api/v2/remarketing/segments.json', expected_status=200,
                            params=params, headers=headers)['items']

        return [s_id['id'] for s_id in ids]

    def get_campaigns_ids_list(self, status):
        params = {
            'fields': 'id,status',
            'limit': 50,
            'sorting': '-id'
        }

        headers = {
            'X-CSRFToken': self.csrf_token,
        }

        ids = self._request('GET', f'api/v2/campaigns.json', expected_status=200,
                            params=params, headers=headers)['items']

        return [s_id['id'] for s_id in ids if (s_id['status'] == status)]

    @allure.step('Creating campaign {campaign_name}')
    def create_campaign(self, campaign_name, file_name, file_path):
        url_id = self.get_url_id('https://google.com/')
        image_600x600_id = self.post_image_upload(file_name, file_path, 600, 600)
        image_1080x607_id = self.post_image_upload(file_name, file_path, 1080, 607)
        icon_256x256_id = self.post_image_upload(file_name, file_path, 256, 256)

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
            'split_audience': [i + 1 for i in range(10)]
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

        campaign_id, banner_ids = self.post_campaign_create(payload)

        return campaign_id, banner_ids

    @allure.step('Deleting campaign id={campaign_id}')
    def delete_campaign(self, campaign_id, banner_ids):
        for b_id in banner_ids:
            self.post_banner_delete(b_id)

        self.post_campaign_delete(campaign_id)

    def check_if_campaign_has_status(self, campaign_id, status):
        return campaign_id in self.get_campaigns_ids_list(status)

    @allure.step('Creating segment {segment_name}')
    def create_segment(self, segment_name, logic_type='or', pass_condition=None):
        relations = [
            {
                'object_type': "remarketing_player",
                'params': {
                    'type': "positive",
                    'left': 150,
                    'right': 25
                }
            },
            {
                'object_type': "remarketing_payer",
                'params': {
                    'type': "positive",
                    'left': 170,
                    'right': 10
                }
            }
        ]

        if logic_type == 'or':
            pass_condition = 1
        elif logic_type == 'and':
            pass_condition = len(relations)
        elif logic_type == 'not':
            pass_condition = 0
        elif logic_type != 'rule':
            raise WrongLogicTypeException

        payload = {
            'logicType': logic_type,
            'name': segment_name,
            'pass_condition': pass_condition,
            'relations': relations
        }

        segment_id = self.post_segment_create(payload)
        return segment_id

    def check_if_segment_exists(self, segment_id):
        return segment_id in self.get_segments_ids_list()
