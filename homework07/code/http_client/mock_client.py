from http_client.base_client import BaseHttpClient


class MockClient(BaseHttpClient):

    def get_surname(self, username):
        r_type = 'GET'
        location = f'/get_surname/{username}'
        headers = {}
        body = {}

        response = self.send_request_json(r_type, location, headers, body)

        return response['status'], response['body']

    def update_surname(self, username, surname):
        r_type = 'PUT'
        location = f'/update_surname/{username}'
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'surname': surname
        }

        response = self.send_request_json(r_type, location, headers, body)

        return response['status'], response['body']

    def delete_surname(self, username):
        r_type = 'DELETE'
        location = f'/delete_surname/{username}'
        headers = {}
        body = {}

        response = self.send_request_json(r_type, location, headers, body)

        return response['status'], response['body']
