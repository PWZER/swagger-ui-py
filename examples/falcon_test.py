import json
import os
from packaging.version import Version
from wsgiref import simple_server

import falcon


class HelloWorldResource(object):
    def on_get(self, req, resp):
        resp.body = json.dumps({'text': 'Hello World!!!'})


app = falcon.API() if Version(falcon.__version__).major < 3 else falcon.App()
app.add_route('/hello/world', HelloWorldResource())

if __name__ == '__main__':
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, 'conf/test.yaml')

    # from swagger_ui import api_doc
    # api_doc(app, config_path=config_path, url_prefix='/api/doc')

    from swagger_ui import falcon_api_doc
    falcon_api_doc(app, config_path=config_path, url_prefix='/api/doc')

    httpd = simple_server.make_server('0.0.0.0', 8989, app)
    httpd.serve_forever()
