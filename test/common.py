import socket
import time
from pathlib import Path

import requests

cur_dir = Path(__file__).resolve().parent

config_path = str(cur_dir.joinpath('conf/test3.yaml'))

mode_list = ['auto', None]

kwargs_list = [
    {
        'url_prefix': '/api/doc',
        'config_path': config_path,
    },
    {
        'url_prefix': '/api/doc',
        'config_path': config_path,
        'editor': True,
    },
    {
        'url_prefix': '/',
        'config_path': config_path,
    },
    {
        'url_prefix': '',
        'config_path': config_path,
    },
    {
        'url_prefix': '/',
        'config_path': config_path,
        'config_rel_url': '/swagger.json',
    },
]


def detect_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', int(port)))
        s.shutdown(2)
        return True
    except Exception:
        return False


def wait_port_listen(port):
    counter = 0
    while counter <= 50:
        if detect_port(port):
            return True
        time.sleep(0.1)
        counter += 1
    return False


def send_requests(port, mode, kwargs):
    assert wait_port_listen(port), 'port: {} not listen!'.format(port)

    url_prefix = 'http://localhost:{}{}'.format(port, kwargs['url_prefix'])
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]
    server_url = 'http://localhost:{}/hello/world'.format(port)

    # Step 1: test server
    assert requests.get(server_url).status_code == 200

    # Step 2: test root
    assert requests.get(url_prefix).status_code == 200
    assert requests.get(url_prefix + '/').status_code == 200

    # Step 3: test static file
    assert requests.get(url_prefix + '/static/LICENSE').status_code == 200

    # Step 4: test editor
    if kwargs.get('editor', False):
        assert requests.get(url_prefix + '/editor').status_code == 200

    # Step 5: test swagger.json
    assert requests.get(url_prefix + '/swagger.json').status_code == 200
