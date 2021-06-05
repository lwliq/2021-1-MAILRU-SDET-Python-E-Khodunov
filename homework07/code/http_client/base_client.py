import logging
import socket
import json


class UnsupportedRequestTypeException(Exception):
    pass


log = logging.getLogger('client')


def create_headers_string(headers: dict):
    if len(headers) == 0:
        return ''

    headers_list = []
    for key in headers.keys():
        headers_list.append(f'{key}: {headers[key]}')

    return '\r\n'.join(headers_list)


def parse_http_response(data: str):
    result = {}
    data = ''.join(data).splitlines()

    start_line = data.pop(0).split(' ')
    result['status'] = {'code': int(start_line[1]), 'text': ' '.join(start_line[2:])}

    result['headers'] = {}

    while True:
        if (line := data.pop(0)) == '':
            break

        line = line.split(' ')
        header = line[0].strip(':')
        value = ' '.join(line[1:])
        result['headers'][header] = value

    if result['headers'].get('Content-Type') == 'application/json':
        result['body'] = json.loads(data.pop())
    else:
        result['body'] = '\n'.join(data)

    return result


class BaseHttpClient:

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = int(port)

    def send_request_json(self, r_type: str, location: str, headers: dict, body: dict):
        supported_types = ('GET', 'POST', 'PUT', 'DELETE')
        if r_type not in supported_types:
            raise UnsupportedRequestTypeException(f'{r_type} type is not supported by client')

        if len(body) > 0:
            body = json.dumps(body)
            headers['Content-Length'] = len(body)
        else:
            body = ''
            headers['Content-Length'] = 0
        headers = create_headers_string(headers)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        sock.connect((self.host, self.port))

        request = f'{r_type} {location} HTTP/1.1\r\nHost:{self.host}\r\n{headers}\r\n\r\n{body}'
        log.info('\nREQUEST\n' + request)
        sock.send(request.encode())

        total_data = ''
        while True:
            data = sock.recv(4096)
            if data:
                total_data += data.decode()
            else:
                sock.close()
                break

        data = parse_http_response(total_data)
        log.info('\nRESPONSE\n' + total_data)
        return data

    def try_connect(self):
        r_type = 'GET'
        location = '/'
        headers = {}
        body = {}

        response = self.send_request_json(r_type, location, headers, body)

        return response['status'], response['body']

    def shutdown_server(self):
        r_type = 'GET'
        location = '/shutdown'
        headers = {}
        body = {}

        response = self.send_request_json(r_type, location, headers, body)

        return response['status'], response['body']
