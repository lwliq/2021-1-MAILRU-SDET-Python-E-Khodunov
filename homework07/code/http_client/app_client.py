from http_client.base_client import BaseHttpClient


class AppClient(BaseHttpClient):

    def add_user(self, username: str):
        r_type = 'POST'
        location = '/add_user'
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'name': username
        }

        response = self.send_request_json(r_type, location, headers, body)

        return response['status'], response['body']

    def get_user(self, username):
        r_type = 'GET'
        location = f'/get_user/{username}'
        headers = {}
        body = {}

        response = self.send_request_json(r_type, location, headers, body)

        return response['status'], response['body']
