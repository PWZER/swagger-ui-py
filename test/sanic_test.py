from pathlib import Path

import pytest
from common import kwargs_list
from common import mode_list
from sanic import Sanic
from sanic import response
from sanic_testing.testing import SanicTestClient


@pytest.fixture(scope="module")
def app():
    app = Sanic("test_sanic")
    return app


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_sanic(app, port, mode, kwargs):
    # app = Sanic(f"server_{port}")

    @app.get(r'/hello/world')
    async def index_handler(request):
        return response.text('Hello World!!!')

    if kwargs["config_rel_url"]:
        @app.get(kwargs["config_rel_url"])
        async def swagger_config_handler(request):
            return response.json(Path(kwargs["config_path"]).read_text())

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import sanic_api_doc
        sanic_api_doc(app, **kwargs)

    url_prefix = kwargs["url_prefix"]
    if url_prefix.endswith("/"):
        url_prefix = url_prefix[:-1]

    client = SanicTestClient(app)
    _, resp = client.get("/hello/world")
    # print(resp.text)
    assert resp.status == 200, resp.text

    _, resp = client.get(url_prefix)
    # print(resp.text)
    assert resp.status == 200, resp.text

    _, resp = client.get(f"{url_prefix}/static/LICENSE")
    # print(resp.text)
    assert resp.status == 200, resp.text

    if kwargs.get("editor"):
        _, resp = client.get(f"{url_prefix}/editor")
        # print(resp.text)
        assert resp.status == 200, resp.text
    else:
        _, resp = client.get(f"{url_prefix}/editor")
        # print(resp.text)
        assert resp.status == 404, resp.text

    _, resp = client.get(f"{url_prefix}/swagger.json")
    # print(resp.text)
    assert resp.status == 200, resp.text
