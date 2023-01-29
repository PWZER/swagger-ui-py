from multiprocessing import Process

import pytest
from common import kwargs_list, mode_list, send_requests


def server_process(port, mode, **kwargs):
    from flask import Flask

    app = Flask(__name__)

    @app.route(r'/hello/world')
    def hello():
        return 'Hello World!!!'

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import flask_api_doc
        flask_api_doc(app, **kwargs)

    app.run(host='localhost', port=port)


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_flask(port, mode, kwargs):
    if kwargs['url_prefix'] in ('/', ''):
        return

    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()
