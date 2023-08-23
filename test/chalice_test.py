import pytest
from chalice import Chalice
from chalice.config import Config
from chalice.local import ForbiddenError
from chalice.local import LocalGateway

from swagger_ui import api_doc
from swagger_ui import chalice_api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    app = Chalice(__name__)

    @app.route('/hello/world')
    def hello():
        return 'Hello World!!!'
    return app


@pytest.mark.parametrize('mode, kwargs', parametrize_list)
def test_chalice(app, mode, kwargs):
    if kwargs.get('config_rel_url'):
        @app.route(kwargs['config_rel_url'])
        def swagger_config_handler():
            return config_content

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        chalice_api_doc(app, **kwargs)

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    client = LocalGateway(app, config=Config())

    headers = {'Host': 'localhost'}

    resp = client.handle_request(
        method='GET', path='/hello/world', headers=headers, body=None)
    assert resp['statusCode'] == 200, resp['body']

    resp = client.handle_request(
        method='GET', path=url_prefix, headers=headers, body=None)
    assert resp['statusCode'] == 200, resp['body']

    resp = client.handle_request(
        method='GET', path=f'{url_prefix}/static/LICENSE',
        headers=headers, body=None)
    assert resp['statusCode'] == 200, resp['body']

    if kwargs.get('editor'):
        resp = client.handle_request(
            method='GET', path=f'{url_prefix}/editor',
            headers=headers, body=None)
        assert resp['statusCode'] == 200, resp['body']
    else:
        try:
            resp = client.handle_request(
                method='GET', path=f'{url_prefix}/editor',
                headers=headers, body=None)
        except ForbiddenError as ex:
            assert "Missing Authentication Token" in str(ex), str(ex)

    if kwargs.get('config_rel_url'):
        resp = client.handle_request(
            method='GET', path=kwargs['config_rel_url'],
            headers=headers, body=None)
        assert resp['statusCode'] == 200, resp['body']
    else:
        resp = client.handle_request(
            method='GET', path=f'{url_prefix}/swagger.json',
            headers=headers, body=None)
        assert resp['statusCode'] == 200, resp['body']
