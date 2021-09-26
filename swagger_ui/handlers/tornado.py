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
        (doc.uri(r''), DocHandler),
        (doc.uri(r'/'), DocHandler),
        (doc.uri(r'/swagger.json'), ConfigHandler),
        (doc.uri(r'/(.+)'), StaticFileHandler, {'path': doc.static_dir}),
    ]

    if doc.editor:
        handlers.insert(1, (doc.uri(r'/editor'), EditorHandler))

    doc.app.add_handlers(r'.*', handlers)


def match(doc):
    try:
        import tornado.web
        if isinstance(doc.app, tornado.web.Application):
            return handler
    except ImportError:
        pass
    return None
