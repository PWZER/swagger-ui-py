from multiprocessing import Process

import pytest
from common import kwargs_list
from common import mode_list
from common import send_requests


def server_process(port, mode, **kwargs):
    import json
    from packaging.version import Version
    from wsgiref import simple_server

    import falcon

    class HelloWorldResource(object):
        def on_get(self, req, resp):
            resp.body = json.dumps({'text': 'Hello World!!!'})

    app = falcon.API() if Version(falcon.__version__).major < 3 else falcon.App()
    app.add_route('/hello/world', HelloWorldResource())

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import falcon_api_doc
        falcon_api_doc(app, **kwargs)

    httpd = simple_server.make_server('localhost', port, app)
    httpd.serve_forever()


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_falcon(port, mode, kwargs):
    if kwargs['url_prefix'] in ('', '/'):
        return

    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()


if __name__ == '__main__':
    kwargs = dict(url_prefix='/api/doc', config_path='conf/test3.yaml')
    # server_process(8090, 'auto', **kwargs)
    server_process(8090, None, **kwargs)
