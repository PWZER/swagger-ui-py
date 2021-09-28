import os
import uvicorn

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse


def hello_world(request):
    return PlainTextResponse('Hello World!!!')


def startup():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cur_dir, 'conf/test.yaml')

    from swagger_ui import api_doc
    api_doc(app, config_path=config_path)


routes = [
    Route('/hello/world', hello_world),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8989, log_level="info")
