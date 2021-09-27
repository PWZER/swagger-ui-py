def handler(doc):
    from tornado.web import RequestHandler, StaticFileHandler

    class DocHandler(RequestHandler):
        def get(self, *args, **kwargs):
            return self.write(doc.doc_html)

    class EditorHandler(RequestHandler):
        def get(self, *args, **kwargs):
            return self.write(doc.editor_html)

    class ConfigHandler(RequestHandler):
        def get(self, *args, **kwargs):
            return self.write(doc.get_config(self.request.host))

    handlers = [
        (doc.root_uri_absolute(slashes=True), DocHandler),
        (doc.root_uri_absolute(slashes=False), DocHandler),
        (doc.swagger_json_uri_absolute, ConfigHandler),
        (r'{}/(.+)'.format(doc.static_uri_absolute),
         StaticFileHandler, {'path': doc.static_dir}),
    ]

    if doc.editor:
        handlers += [
            (doc.editor_uri_absolute(slashes=True), EditorHandler),
            (doc.editor_uri_absolute(slashes=False), EditorHandler),
        ]

    doc.app.add_handlers(r'.*', handlers)


def match(doc):
    try:
        import tornado.web
        if isinstance(doc.app, tornado.web.Application):
            return handler
    except ImportError:
        pass
    return None
