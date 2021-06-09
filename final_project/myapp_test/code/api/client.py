import logging

import requests
from urllib.parse import urljoin
from utils.decorators import wait
from requests.exceptions import ConnectionError


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):

        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger('api_client')

    def _request(self, request_type, location, expected_status=None, **kwargs):
        url = urljoin(self.base_url, location)
        response = self.session.request(request_type, url, **kwargs)
        headers = '\n'.join(['{}: {}'.format(*hv) for hv in response.request.headers.items()])
        self.logger.info('\nREQUEST\n'
                         + f'{response.request.url}\n'
                         + f'{headers}\n\n'
                         + f'{response.request.body}\n'
                         )

        headers = '\n'.join(['{}: {}'.format(*hv) for hv in response.headers.items()])
        self.logger.info('\nRESPONSE\n'
                         + f'{response.status_code} {response.reason}\n'
                         + f'{headers}\n\n'
                         + f'{response.text[:100] if response.text is not None else response.text}\n'
                         )
        if expected_status:
            if response.status_code != expected_status:
                raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        return response

    def wait_for_app(self):
        wait(
            method=self._request,
            error=ConnectionError,
            timeout=20,
            interval=0.2,
            check=False,
            request_type='GET',
            location='status',
        )

    def login(self, username, password):

        data = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive'
        }

        # Collecting session cookie
        response = wait(
            method=self._request,
            error=ResponseStatusCodeException,
            timeout=10,
            interval=0.2,
            check=False,
            request_type='POST',
            location='login',
            expected_status=302,
            data=data,
            headers=headers,
            allow_redirects=False
        )

        return response

    def get_status(self):
        return self._request('GET', 'status')

    def delete_user(self, username):
        return self._request('GET', f'api/del_user/{username}')

    def block_user(self, username):
        return self._request('GET', f'api/block_user/{username}')

    def accept_user(self, username):
        return self._request('GET', f'api/accept_user/{username}')

    def add_user(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive'
        }

        return self._request('POST', f'api/add_user', headers=headers, json=payload)

