import pytest
from bottle import Bottle
from webtest import AppError
from webtest import TestApp

from swagger_ui import api_doc
from swagger_ui import bottle_api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    app = Bottle()

    @app.route('/hello/world')
    def hello():
        return 'Hello World!!!'
    return app


@pytest.mark.parametrize('mode, kwargs', parametrize_list)
def test_bottle(app, mode, kwargs):
    if kwargs.get('config_rel_url'):
        @app.route(kwargs['config_rel_url'])
        def swagger_config_handler():
            return config_content

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        bottle_api_doc(app, **kwargs)

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    client = TestApp(app)

    resp = client.get('/hello/world')
    assert resp.status_code == 200, resp.data

    resp = client.get(url_prefix)
    assert resp.status_code == 200, resp.data

    resp = client.get(f'{url_prefix}/static/LICENSE')
    assert resp.status_code == 200, resp.data

    if kwargs.get('editor'):
        resp = client.get(f'{url_prefix}/editor')
        assert resp.status_code == 200, resp.data
    else:
        try:
            resp = client.get(f'{url_prefix}/editor')
        except AppError as ex:
            assert '404 Not Found' in str(ex), str(ex)

    if kwargs.get('config_rel_url'):
        resp = client.get(kwargs['config_rel_url'])
        assert resp.status_code == 200, resp.data
    else:
        resp = client.get(f'{url_prefix}/swagger.json')
        assert resp.status_code == 200, resp.data
