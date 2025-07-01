import json

from packaging.version import Version


class FalconInterface(object):
    def __init__(self, version: str, use_async=False):
        self.version = version
        self.use_async = use_async

    def handler(self, doc):
        interface = self

        class Handler(object):
            async def on_get_async(self, req, resp):
                self.on_get(req, resp)

        class SwaggerDocHandler(Handler):
            def on_get(self, req, resp):
                resp.content_type = 'text/html'
                if Version(interface.version) >= Version('4.0.0'):
                    resp.data = doc.doc_html.encode()
                else:
                    resp.body = doc.doc_html

        class SwaggerEditorHandler(Handler):
            def on_get(self, req, resp):
                resp.content_type = 'text/html'
                if Version(interface.version) >= Version('4.0.0'):
                    resp.data = doc.editor_html.encode()
                else:
                    resp.body = doc.editor_html

        class SwaggerConfigHandler(Handler):
            def on_get(self, req, resp):
                resp.content_type = 'application/json'
                if Version(interface.version) >= Version('4.0.0'):
                    resp.media = doc.get_config(f'{req.host}:{req.port}')
                else:
                    resp.body = json.dumps(doc.get_config(f'{req.host}:{req.port}'))

        suffix = 'async' if self.use_async else None
        doc.app.add_route(doc.root_uri_absolute(slashes=True),
                          SwaggerDocHandler(), suffix=suffix)
        doc.app.add_route(doc.root_uri_absolute(slashes=False),
                          SwaggerDocHandler(), suffix=suffix)

        if doc.editor:
            doc.app.add_route(doc.editor_uri_absolute(slashes=True),
                              SwaggerEditorHandler(), suffix=suffix)
            doc.app.add_route(doc.editor_uri_absolute(slashes=False),
                              SwaggerEditorHandler(), suffix=suffix)

        if doc.config_rel_url is None:
            doc.app.add_route(doc.swagger_json_uri_absolute, SwaggerConfigHandler(), suffix=suffix)
        doc.app.add_static_route(
            prefix=doc.static_uri_absolute,
            directory='{}/'.format(doc.static_dir),
            downloadable=True,
        )


def match(doc):
    try:
        import falcon

        interface = None
        if Version(falcon.__version__) >= Version('3.0.0'):
            import falcon.asgi
            if isinstance(doc.app, falcon.asgi.App):
                interface = FalconInterface(version=falcon.__version__, use_async=True)
            elif isinstance(doc.app, falcon.App):
                interface = FalconInterface(version=falcon.__version__, use_async=False)
        else:
            if isinstance(doc.app, falcon.API):
                interface = FalconInterface(version=falcon.__version__, use_async=False)

        if interface:
            return interface.handler
    except ImportError:
        pass
    return None
