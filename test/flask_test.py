import pytest
from flask import Flask

from swagger_ui import api_doc
from swagger_ui import flask_api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route(r'/hello/world')
    def hello():
        return 'Hello World!!!'
    return app


@pytest.mark.parametrize('mode, kwargs', parametrize_list)
def test_flask(app, mode, kwargs):
    if kwargs['url_prefix'] in ('/', ''):
        return

    if kwargs.get('config_rel_url'):
        @app.route(kwargs['config_rel_url'])
        def swagger_config():
            return config_content

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        flask_api_doc(app, **kwargs)

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    client = app.test_client()

    resp = client.get('/hello/world')
    assert resp.status_code == 200, resp.data

    resp = client.get(url_prefix)
    assert resp.status_code == 200, resp.data

    resp = client.get(f'{url_prefix}/static/LICENSE')
    assert resp.status_code == 200, resp.data

    resp = client.get(f'{url_prefix}/editor')
    if kwargs.get('editor'):
        assert resp.status_code == 200, resp.data
    else:
        assert resp.status_code == 404, resp.data

    if kwargs.get('config_rel_url'):
        resp = client.get(kwargs['config_rel_url'])
        assert resp.status_code == 200, resp.data
    else:
        resp = client.get(f'{url_prefix}/swagger.json')
        assert resp.status_code == 200, resp.data
