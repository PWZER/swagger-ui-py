def handler(doc):
    from bottle import static_file, request

    @doc.app.get(doc.root_uri_absolute(slashes=True))
    @doc.app.get(doc.root_uri_absolute(slashes=False))
    def index():
        return doc.doc_html

    @doc.app.get(doc.swagger_json_uri_absolute)
    def config_handler():
        return doc.get_config(request.urlparts.netloc)

    @doc.app.get(r'{}/<filepath>'.format(doc.static_uri_absolute))
    def java_script_file(filepath):
        return static_file(filepath, root=doc.static_dir)

    if doc.editor:
        @doc.app.get(doc.editor_uri_absolute(slashes=True))
        @doc.app.get(doc.editor_uri_absolute(slashes=False))
        def editor():
            return doc.editor_html


def match(doc):
    try:
        from bottle import Bottle
        if isinstance(doc.app, Bottle):
            return handler
    except ImportError:
        pass
    return None
