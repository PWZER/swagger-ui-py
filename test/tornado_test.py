import pytest
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web

from swagger_ui import api_doc
from swagger_ui import tornado_api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    class HelloWorldHandler(tornado.web.RequestHandler):
        def get(self, *args, **kwargs):
            return self.write('Hello World!!!')

    app = tornado.web.Application([
        (r'/hello/world', HelloWorldHandler),
    ])
    return app


@pytest.mark.asyncio
@pytest.mark.parametrize('mode, kwargs', parametrize_list)
async def test_tornado(app, mode, kwargs):
    if kwargs.get('config_rel_url'):
        class SwaggerConfigHandler(tornado.web.RequestHandler):
            def get(self, *args, **kwargs):
                return self.write(config_content)
        app.add_handlers('.*', [(kwargs['config_rel_url'], SwaggerConfigHandler)])

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        tornado_api_doc(app, **kwargs)

    server = tornado.httpserver.HTTPServer(app)
    server.listen(0)

    host, port = list(server._sockets.values())[0].getsockname()
    server_addr = f'http://{host}:{port}'

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]
    url_prefix = f'{server_addr}{url_prefix}'

    http_client = tornado.httpclient.AsyncHTTPClient()

    resp = await http_client.fetch(f'{server_addr}/hello/world')
    assert resp.code == 200, resp.body

    resp = await http_client.fetch(url_prefix)
    assert resp.code == 200, resp.body

    resp = await http_client.fetch(f'{url_prefix}/static/LICENSE')
    assert resp.code == 200, resp.body

    if kwargs.get('editor'):
        resp = await http_client.fetch(f'{url_prefix}/editor')
        assert resp.code == 200, resp.body
    else:
        try:
            resp = await http_client.fetch(f'{url_prefix}/editor')
        except tornado.httpclient.HTTPClientError as e:
            assert e.code == 404, e.response.body

    if kwargs.get('config_rel_url'):
        resp = await http_client.fetch(server_addr + kwargs['config_rel_url'])
        assert resp.code == 200, resp.body
    else:
        resp = await http_client.fetch(f'{url_prefix}/swagger.json')
        assert resp.code == 200, resp.body
