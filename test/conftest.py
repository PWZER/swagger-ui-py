import socket
import pytest


@pytest.fixture(scope='function')
def port():
    sock = socket.socket()
    sock.bind(('', 0))
    ip, port = sock.getsockname()
    sock.close()
    return port
