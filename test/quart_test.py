import pytest
from quart import Quart

from swagger_ui import api_doc
from swagger_ui import quart_api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    app = Quart(__name__)

    @app.route(r'/hello/world', methods=['GET'])
    async def hello():
        return 'Hello World!!!'
    return app


@pytest.mark.asyncio
@pytest.mark.parametrize('mode, kwargs', parametrize_list)
async def test_quart(app, mode, kwargs):
    if kwargs['url_prefix'] in ('/', ''):
        return

    if kwargs.get('config_rel_url'):
        @app.route(kwargs['config_rel_url'], methods=['GET'])
        def swagger_config():
            return config_content

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        quart_api_doc(app, **kwargs)

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    client = app.test_client()

    resp = await client.get('/hello/world', follow_redirects=True)
    assert resp.status_code == 200, await resp.get_data()

    resp = await client.get(url_prefix, follow_redirects=True)
    assert resp.status_code == 200, await resp.get_data()

    resp = await client.get(f'{url_prefix}/static/LICENSE', follow_redirects=True)
    assert resp.status_code == 200, await resp.get_data()

    resp = await client.get(f'{url_prefix}/editor', follow_redirects=True)
    if kwargs.get('editor'):
        assert resp.status_code == 200, await resp.get_data()
    else:
        assert resp.status_code == 404, await resp.get_data()

    if kwargs.get('config_rel_url'):
        resp = await client.get(kwargs['config_rel_url'], follow_redirects=True)
        assert resp.status_code == 200, await resp.get_data()
    else:
        resp = await client.get(f'{url_prefix}/swagger.json', follow_redirects=True)
        assert resp.status_code == 200, await resp.get_data()
