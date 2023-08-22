from multiprocessing import Process

import pytest
from common import kwargs_list
from common import mode_list
from common import send_requests


def server_process(port, mode, **kwargs):
    import uvicorn
    from starlette.applications import Starlette
    from starlette.responses import PlainTextResponse
    from starlette.routing import Route

    def hello_world(request):
        return PlainTextResponse('Hello World!!!')

    def startup():
        if mode == 'auto':
            from swagger_ui import api_doc
            api_doc(app, **kwargs)
        else:
            from swagger_ui import starlette_api_doc
            starlette_api_doc(app, **kwargs)

    routes = [
        Route('/hello/world', hello_world),
    ]

    app = Starlette(debug=True, routes=routes, on_startup=[startup])
    uvicorn.run(app, host="localhost", port=port, log_level="info")


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_starlette(port, mode, kwargs):
    if kwargs['url_prefix'] in ('/', ''):
        return

    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()
