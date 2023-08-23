import pytest
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from swagger_ui import api_doc
from swagger_ui import starlette_api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    app = Starlette()

    @app.route('/hello/world')
    def hello_world(request):
        return PlainTextResponse('Hello World!!!')
    return app


@pytest.mark.parametrize('mode, kwargs', parametrize_list)
def test_starlette(app, mode, kwargs):
    if kwargs['url_prefix'] in ('/', ''):
        return

    if kwargs.get('config_rel_url'):
        @app.route(kwargs['config_rel_url'])
        def swagger_config(request):
            return PlainTextResponse(config_content)

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        starlette_api_doc(app, **kwargs)

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    client = TestClient(app)

    resp = client.get('/hello/world')
    assert resp.status_code == 200, resp.text

    resp = client.get(url_prefix)
    assert resp.status_code == 200, resp.text

    resp = client.get(f'{url_prefix}/static/LICENSE')
    assert resp.status_code == 200, resp.text

    if kwargs.get('editor'):
        resp = client.get(f'{url_prefix}/editor')
        assert resp.status_code == 200, resp.text
    else:
        resp = client.get(f'{url_prefix}/editor')
        assert resp.status_code == 404, resp.text

    if kwargs.get('config_rel_url'):
        resp = client.get(kwargs['config_rel_url'])
        assert resp.status_code == 200, resp.text
    else:
        resp = client.get(f'{url_prefix}/swagger.json')
        assert resp.status_code == 200, resp.text
