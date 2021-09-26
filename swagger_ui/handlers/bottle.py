def handler(doc):
    from bottle import static_file, request

    @doc.app.get(doc.uri())
    @doc.app.get(doc.uri(r'/'))
    def index():
        return doc.doc_html

    @doc.app.get(doc.uri(r'/swagger.json'))
    def config_handler():
        return doc.get_config(request.urlparts.netloc)

    @doc.app.get(doc.uri(r'/<filepath>'))
    def java_script_file(filepath):
        return static_file(filepath, root=doc.static_dir)

    if doc.editor:
        @doc.app.get(doc.uri(r'/editor'))
        @doc.app.get(doc.uri(r'/editor/'))
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
