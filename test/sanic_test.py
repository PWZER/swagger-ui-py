from multiprocessing import Process

import pytest
from common import kwargs_list, mode_list, send_requests


def server_process(port, mode, **kwargs):
    from sanic import Sanic, response

    app = Sanic(__name__)

    @app.get(r'/hello/world')
    async def index_handler(request):
        return response.text('Hello World!!!')

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import sanic_api_doc
        sanic_api_doc(app, **kwargs)
    app.run(host='localhost', port=port)


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_sanic(port, mode, kwargs):
    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()
