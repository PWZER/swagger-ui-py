import os

from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


app = web.Application()
app.add_routes([web.get('/hello/world', hello)])


if __name__ == '__main__':
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, 'conf/test.yaml')

    from swagger_ui import api_doc
    api_doc(app, config_path=config_path)
    web.run_app(app, port=8989)
