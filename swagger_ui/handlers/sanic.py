def handler(doc):
    from sanic import response
    from sanic.blueprints import Blueprint

    swagger_blueprint = Blueprint(
        'swagger_blueprint',
        url_prefix=doc.url_prefix,
        strict_slashes=False,
    )

    @swagger_blueprint.get(doc.root_uri_relative(slashes=True))
    async def swagger_blueprint_doc_handler(request):
        return response.html(doc.doc_html)

    if doc.editor:
        @swagger_blueprint.get(doc.editor_uri_relative(slashes=True))
        async def swagger_blueprint_editor_handler(request):
            return response.html(doc.editor_html)

    @swagger_blueprint.get(doc.swagger_json_uri_relative)
    async def swagger_blueprint_config_handler(request):
        return response.json(doc.get_config(request.host))

    swagger_blueprint.static(doc.static_uri_relative, doc.static_dir)
    doc.app.blueprint(swagger_blueprint)


def match(doc):
    try:
        import sanic
        if isinstance(doc.app, sanic.Sanic):
            return handler
    except ImportError:
        pass
    return None
