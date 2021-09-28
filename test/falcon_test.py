import pytest
from multiprocessing import Process

from common import send_requests, mode_list, kwargs_list


def server_process(port, mode, **kwargs):
    import json
    import falcon
    from distutils.version import StrictVersion
    from wsgiref import simple_server

    class HelloWorldResource(object):
        def on_get(self, req, resp):
            resp.body = json.dumps({'text': 'Hello World!!!'})

    if StrictVersion(falcon.__version__) < StrictVersion('3.0.0'):
        app = falcon.API()
    else:
        app = falcon.App()

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
