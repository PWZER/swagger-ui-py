from multiprocessing import Process

import pytest
from common import kwargs_list
from common import mode_list
from common import send_requests


def server_process(port, mode, **kwargs):
    from aiohttp import web

    async def hello(request):
        return web.Response(text="Hello, world")

    app = web.Application()
    app.add_routes([web.get('/hello/world', hello)])

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import aiohttp_api_doc
        aiohttp_api_doc(app, **kwargs)
    web.run_app(app, host='localhost', port=port)


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_aiohttp(port, mode, kwargs):
    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()
