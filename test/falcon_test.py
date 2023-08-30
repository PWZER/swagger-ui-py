import falcon
import pytest
from falcon import testing
from packaging.version import Version

from swagger_ui import api_doc
from swagger_ui import falcon_api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    class HelloWorldHandler(object):
        def on_get(self, req, resp):
            resp.body = 'Hello World!!!'

    if Version(falcon.__version__) < Version('3.0.0'):
        app = falcon.API()
    else:
        app = falcon.App()

    app.add_route('/hello/world', HelloWorldHandler())
    return app


@pytest.mark.parametrize('mode, kwargs', parametrize_list)
def test_falcon(app, mode, kwargs):
    if kwargs['url_prefix'] in ('', '/'):
        return

    if kwargs.get('config_rel_url'):
        class SwaggerConfigHandler(object):
            def on_get(self, req, resp):
                resp.body = config_content
        app.add_route(kwargs['config_rel_url'], SwaggerConfigHandler())

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        falcon_api_doc(app, **kwargs)

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    client = testing.TestClient(app)

    resp = client.get('/hello/world')
    assert resp.status_code == 200, resp.text

    resp = client.get(url_prefix)
    assert resp.status_code == 200, resp.text

    resp = client.get(f'{url_prefix}/static/LICENSE')
    assert resp.status_code == 200, resp.text

    resp = client.get(f'{url_prefix}/editor')
    if kwargs.get('editor'):
        assert resp.status_code == 200, resp.text
    else:
        assert resp.status_code == 404, resp.text

    if kwargs.get('config_rel_url'):
        resp = client.get(kwargs['config_rel_url'])
        assert resp.status_code == 200, resp.text
    else:
        resp = client.get(f'{url_prefix}/swagger.json')
        assert resp.status_code == 200, resp.text
