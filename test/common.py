import time
import socket
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
config_path = str(cur_dir.joinpath('conf/test3.yaml'))


mode_list = ['auto', None]

kwargs_list = [
    {
        'url_prefix': '/api/doc',
        'config_path': config_path,
    },
    {
        'url_prefix': '/',
        'config_path': config_path,
    },
    {
        'url_prefix': '',
        'config_path': config_path,
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
