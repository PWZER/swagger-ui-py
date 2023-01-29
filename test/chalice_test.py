from multiprocessing import Process

import pytest
from common import kwargs_list, mode_list, send_requests


def server_process(port, mode, **kwargs):
    from chalice import Chalice
    from chalice.config import Config
    from chalice.local import create_local_server

    app = Chalice(__name__)

    @app.route('/hello/world')
    def index():
        return {'hello': 'world'}

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import chalice_api_doc
        chalice_api_doc(app, **kwargs)

    config = Config()
    create_local_server(app, config, 'localhost', port).serve_forever()


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_chalice(port, mode, kwargs):
    if kwargs['url_prefix'] in ('/', ''):
        return

    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()
