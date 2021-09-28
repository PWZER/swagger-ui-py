import pytest
from multiprocessing import Process

from common import send_requests, mode_list, kwargs_list


def server_process(port, mode, **kwargs):
    from quart import Quart

    app = Quart(__name__)

    @app.route(r'/hello/world', methods=['GET'])
    async def index_handler():
        return 'Hello World!!!'

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import quart_api_doc
        quart_api_doc(app, **kwargs)
    app.run(host='0.0.0.0', port=port)


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_quart(port, mode, kwargs):
    if kwargs['url_prefix'] in ('/', ''):
        return

    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()
