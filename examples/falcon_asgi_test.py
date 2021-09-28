import os
import json
import uvicorn
import falcon.asgi


class HelloWorldResource(object):
    async def on_get(self, req, resp):
        resp.body = json.dumps({'text': 'Hello World!!!'})


def create_app():
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, 'conf/test.yaml')

    app = falcon.asgi.App()
    app.add_route('/hello/world', HelloWorldResource())

    from swagger_ui import api_doc
    api_doc(app, config_path=config_path, url_prefix='/api/doc')
    return app


uvicorn.run(create_app(), host="0.0.0.0", port=8989, log_level="info")
