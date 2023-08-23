import pytest
from aiohttp import web

from swagger_ui import aiohttp_api_doc
from swagger_ui import api_doc

from .common import config_content
from .common import parametrize_list


@pytest.fixture
def app():
    async def hello(request):
        return web.Response(text="Hello, world")

    app = web.Application()
    app.add_routes([web.get('/hello/world', hello)])
    return app


@pytest.mark.asyncio
@pytest.mark.parametrize('mode, kwargs', parametrize_list)
async def test_aiohttp(app, aiohttp_client, mode, kwargs):
    if kwargs.get('config_rel_url'):
        async def swagger_config_handler(request):
            return web.Response(text=config_content)
        app.add_routes([web.get(kwargs['config_rel_url'], swagger_config_handler)])

    if mode == 'auto':
        api_doc(app, **kwargs)
    else:
        aiohttp_api_doc(app, **kwargs)

    url_prefix = kwargs['url_prefix']
    if url_prefix.endswith('/'):
        url_prefix = url_prefix[:-1]

    client = await aiohttp_client(app)

    resp = await client.get('/hello/world')
    assert resp.status == 200, await resp.text()

    resp = await client.get(url_prefix)
    assert resp.status == 200, await resp.text()

    resp = await client.get(f'{url_prefix}/static/LICENSE')
    assert resp.status == 200, await resp.text()

    if kwargs.get('editor'):
        resp = await client.get(f'{url_prefix}/editor')
        assert resp.status == 200, await resp.text()
    else:
        resp = await client.get(f'{url_prefix}/editor')
        assert resp.status == 404, await resp.text()

    if kwargs.get('config_rel_url'):
        resp = await client.get(kwargs['config_rel_url'])
        assert resp.status == 200, await resp.text()
    else:
        resp = await client.get(f'{url_prefix}/swagger.json')
        assert resp.status == 200, await resp.text()
