import pytest
import requests
from multiprocessing import Process

from common import wait_port_listen, mode_list, kwargs_list


def server_process(port, mode, **kwargs):
    import tornado.ioloop
    import tornado.web

    class HelloWorldHandler(tornado.web.RequestHandler):
        def get(self, *args, **kwargs):
            return self.write('Hello World!!!')

    app = tornado.web.Application([
        (r'/hello/world', HelloWorldHandler),
    ])

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import tornado_api_doc
        tornado_api_doc(app, **kwargs)

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_tornado(port, mode, kwargs):
    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()

    assert wait_port_listen(port), 'port: {} not listen!'.format(port)

    url_prefix = 'http://127.0.0.1:{}{}'.format(port, kwargs['url_prefix'])
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]
    server_url = 'http://127.0.0.1:{}/hello/world'.format(port)

    # Step 1: test server
    assert requests.get(server_url).status_code == 200

    # Step 2: test root
    assert requests.get(url_prefix).status_code == 200
    assert requests.get(url_prefix + '/').status_code == 200

    # Step 3: test static file
    assert requests.get(url_prefix + '/static/LICENSE').status_code == 200

    # Step 4: test editor
    if kwargs.get('editor', False):
        assert requests.get(url_prefix + '/editor').status_code == 200

    # Step 5: test swagger.json
    if kwargs.get('editor', False):
        assert requests.get(url_prefix + '/swagger.json').status_code == 200

    proc.terminate()
