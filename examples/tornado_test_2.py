import json
import os

import tornado.ioloop
import tornado.web


class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.write('Hello World!!!')


def make_app():
    return tornado.web.Application([
        (r'/hello/world', HelloWorldHandler),
    ])


if __name__ == '__main__':
    app = make_app()

    from swagger_ui import api_doc
    spec_string = '{"paths": {"/random": {"get": {"description": "Get a random pet", "security": [{"ApiKeyAuth": []}],' \
                  ' "responses": {"200": {"description": "Return a pet", "content": {"application/json":' \
                  ' {"schema": {"$ref": "#/components/schemas/Pet"}}}}}}}}, ' \
                  '"info": {"title": "Swagger Petstore", "version": "1.0.0"},' \
                  ' "openapi": "3.0.0", "servers" : [ {"url": "http://127.0.0.1:8989/api"}],' \
                  ' "components": {"schemas": {"Category": {"type": "object", "properties": ' \
                  '{"id": {"type": "integer"}, "name": {"type": "string"}}, "required": ["name"]}, "Pet": ' \
                  '{"type": "object", "properties": {"categories": {"type": "array", "items": ' \
                  '{"$ref": "#/components/schemas/Category"}}, "name": {"type": "string"}}}}, "securitySchemes": ' \
                  '{"ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-Key"}}}}'
    api_doc(app, spec=spec_string, url_prefix='/api/doc/')

    app.listen(8989)
    tornado.ioloop.IOLoop.current().start()
